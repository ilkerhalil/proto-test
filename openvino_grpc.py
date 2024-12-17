# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: openvino.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import openvino_pb2


class OpenvinoServiceBase(abc.ABC):

    @abc.abstractmethod
    async def Predict(self, stream: 'grpclib.server.Stream[openvino_pb2.ImageChunk, openvino_pb2.PredictResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/openvino.OpenvinoService/Predict': grpclib.const.Handler(
                self.Predict,
                grpclib.const.Cardinality.STREAM_UNARY,
                openvino_pb2.ImageChunk,
                openvino_pb2.PredictResponse,
            ),
        }


class OpenvinoServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Predict = grpclib.client.StreamUnaryMethod(
            channel,
            '/openvino.OpenvinoService/Predict',
            openvino_pb2.ImageChunk,
            openvino_pb2.PredictResponse,
        )
