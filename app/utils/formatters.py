
from whisper.utils import ResultWriter, WriteTXT, WriteSRT, WriteVTT, WriteTSV, WriteJSON
from typing import BinaryIO, Union
from hashlib import md5
from time import localtime


def write_result(result: dict, file: BinaryIO, output: Union[str, None]):
    if(output == "srt"):
        WriteSRT(ResultWriter).write_result(result, file=file)
    elif(output == "vtt"):
        WriteVTT(ResultWriter).write_result(result, file=file)
    elif(output == "tsv"):
        WriteTSV(ResultWriter).write_result(result, file=file)
    elif(output == "json"):
        WriteJSON(ResultWriter).write_result(result, file=file)
    elif(output == "txt"):
        WriteTXT(ResultWriter).write_result(result, file=file)
    else:
        raise ValueError("Provide a valid output option")


def prepend_unique_name(filename: str):
    prefix = md5(str(localtime()).encode('utf-8')).hexdigest()
    return f"{prefix}_{filename}"
