from grpclib.utils import graceful_exit
from grpclib.server import Server
import openvino_pb2
from openvino_grpc import OpenvinoServiceBase
import asyncio

class OpenvinoServiceImpl(OpenvinoServiceBase):
    async def Predict(self, stream):
        image_chunks = []

        try:
            # Receive all chunks
            async for chunk in stream:
                image_chunks.append(chunk.chunk_data)
                if chunk.is_last:
                    break

            # Combine chunks
            complete_image = b''.join(image_chunks)

            # Process image
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(complete_image))

            response = openvino_pb2.PredictResponse(
                haserror=False,
                errormessage="",
                duration=1.0,
                citizenship_number="123456789"
            )
            await stream.send_message(response)

        except Exception as e:
            response = openvino_pb2.PredictResponse(
                haserror=True,
                errormessage=str(e),
                duration=0.0,
                citizenship_number=""
            )
            await stream.send_message(response)

# Server setup
async def serve():
    server = Server([OpenvinoServiceImpl()])

    with graceful_exit([server]):
        await server.start('0.0.0.0', 50051)
        print(f"Server started at 0.0.0.0:50051")
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(serve())