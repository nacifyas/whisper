from fastapi import FastAPI, File, Query, UploadFile, WebSocket, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from core.transcriptor import transcribe
from config.env import Settings
import uvicorn
import logging
import os
from whisper.tokenizer import LANGUAGES
from threading import Lock
from utils.files import load
from core.whisper import model


app = FastAPI()


@app.on_event("startup")
async def logging_setup() -> None:
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} {asctime} {message}",
        style="{",
        use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)


@app.on_event("startup")
async def audio_dir_setup() -> None:
    audio_dir = Settings().audio_dir
    os.makedirs(audio_dir, exist_ok=True)



html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Transcriptorrrr</title>
</head>
<body>
    <h1>Transcriptorrrrr</h1>
    <select id="elementDropdown"></select> <input type="text" id="stringInput"> <button id="uploadFileButton">Upload Audio/Video</button>
    <ul id='messages'>
    </ul>
    <script>
        let ws = null; // Global WebSocket object for clarity

        // Replace with your list of elements for the dropdown
        const elementsList = {list(LANGUAGES.keys())};

        window.addEventListener('load', function() {{
            ws = new WebSocket("ws://whisper.atomflare.net/ws");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            }};

            // Create the dropdown element
            const dropdown = document.getElementById("elementDropdown");
            elementsList.forEach(element => {{
                const option = document.createElement("option");
                option.value = element;
                option.text = element;
                dropdown.appendChild(option);
            }});

            // Create the input field for string
            const inputField = document.getElementById("stringInput");

            // Update function to validate only numbers, chars, and spaces, or allow empty
            function validateString(str) {{
                return str.length === 0 || /^[a-zA-Z0-9 ]+$/.test(str);
            }}

            // Add event listener for upload button
            document.getElementById("uploadFileButton").addEventListener("click", async function() {{
                // Create a temporary file input element
                const fileInput = document.createElement("input");
                fileInput.type = "file";
                fileInput.style.display = "none";
                fileInput.accept = "audio/*, video/*"; // Adjust accepted file types

                // Trigger file selection prompt
                fileInput.click();

                // Handle file selection
                fileInput.addEventListener("change", async function(event) {{
                    const selectedFile = event.target.files[0];
                    if (!selectedFile) {{
                        return; // No file selected
                    }}

                    // Create a FormData object with the file and additional data
                    const formData = new FormData();
                    formData.append("file", selectedFile);

                    // Validate input string before sending data
                    const inputValue = document.getElementById("stringInput").value;
                    if (!validateString(inputValue)) {{
                        console.error("Invalid input: Only numbers, chars, and spaces allowed.");
                        return;
                    }}

                    const selectedElement = document.getElementById("elementDropdown").value;

                    try {{
                        const response = await fetch("/upload", {{
                            method: "POST",
                            body: formData
                        }});

                        const data = await response.json();
                        console.log(data);
                        if (data.success) {{
                            console.log("File uploaded successfully");
                            if (ws && ws.readyState === WebSocket.OPEN) {{
                                const message = `${{data.file_path}},${{selectedElement}},${{inputValue}}`;
                                ws.send(message); // Send combined message through websocket
                            }} else {{
                                console.error("WebSocket connection not established or closed");
                                // Handle the case where the connection isn't ready
                            }}
                        }} else {{
                            console.error("Error uploading file:", data.error);
                            // Show an error message to the user
                        }}
                    }} catch (error) {{
                        console.error("Error sending file:", error);
                        // Show an error message to the user
                    }}
                }});

                // Add the temporary file input to the document and remove it afterward
                document.body.appendChild(fileInput);
                fileInput.remove();
            }});
        }});
    </script>
</body>
</html>
"""


@app.get("/", response_class=RedirectResponse, include_in_schema=False, status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def index() -> str:
    return "/home"


@app.get("/home", status_code=status.HTTP_200_OK)
async def home():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        mss = await websocket.receive_text()
        print(mss)
        if "," in mss:
            file_route, language, initial_prompt = mss.split(",")
            with Lock():
                segment_generator, _ = model.transcribe(file_route,
                                                        language=language if language in LANGUAGES.keys() else None,
                                                        initial_prompt=initial_prompt,
                                                        )
                for segment in segment_generator:
                    await websocket.send_text(segment.text)


@app.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def transcriptor(file: UploadFile = File(...)):
    file_path = load(file)
    return {"success": True, "file_path": file_path}


@app.post("/asr", status_code=status.HTTP_200_OK)
def automatic_speech_recognition(
    output_language: str | None = Query(default=None, enum=[*LANGUAGES.keys()]),
    description: str | None = None,
    file: UploadFile = File(...),
    output_format: str = Query(default="txt", enum=["txt", "vtt", "srt", "tsv", "json"]),
    word_timestamps: bool = False
) -> StreamingResponse:
    res = transcribe(file, language=output_language, word_timestamps=word_timestamps, initial_prompt=description, output_format=output_format)
    return StreamingResponse(
        res,
        media_type="text/plain",
        headers={
                'Asr-Engine': "openai/whisper",
                'Content-Disposition': f'attachment; filename="{file.filename}.{output_format}"'
        }
    )

    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=Settings().dev_mode)
