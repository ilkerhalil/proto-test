import asyncio
from grpclib.client import Channel
from openvino_pb2 import ImageChunk, PredictResponse
from openvino_grpc import OpenvinoServiceStub

CHUNK_SIZE = 1024 * 1024  # 1MB chunks

async def predict_image(image_path: str):
    async with Channel('0.0.0.0', 50051) as channel:
        service = OpenvinoServiceStub(channel)

        # Create async generator for chunks
        async def chunk_generator():
            with open(image_path, 'rb') as f:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        yield ImageChunk(chunk_data=b'', is_last=True)
                        break
                    yield ImageChunk(chunk_data=chunk, is_last=False)

        try:
            # Create stream and send chunks
            async with service.Predict.open() as stream:
                async for chunk in chunk_generator():
                    await stream.send_message(chunk)
                await stream.end()

                # Receive response
                response = await stream.recv_message()
                return response

        except Exception as e:
            print(f"Error during streaming: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        response = asyncio.run(predict_image("test.png"))
        if response.haserror:
            print(f"Error: {response.errormessage}")
        else:
            print(f"Prediction successful!")
            print(f"Citizenship Number: {response.citizenship_number}")
            print(f"Duration: {response.duration}s")
    except Exception as e:
        print(f"Failed to process image: {str(e)}")