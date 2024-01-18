import os
import time
from flask import request
from flask_restx import Resource, Namespace, fields

from handlers import Logger
from facefusion import core

logging = Logger.set_logger(log_name='Server', filename='logs/server.log')

Infer = Namespace(
    name="ENLIPLE",
    description="Enliple Face Swap 위한 API"
)

params = Infer.model('Source Path', {  # Model 객체 생성
    'source': fields.String(description='Main Image', required=True, example="/workspace/data/video_img/0.jpg"),
    'target': fields.String(description='Change Image', required=True, example="/workspace/data/video_img/13.jpeg")
})

@Infer.route('/status')
class HealthCheck(Resource):
    def get(self):
        result = {"status": "OK", "version": "0.1"}
        return result

@Infer.route("/api/face-generation")
class FaceSwapGeneration(Resource):
    @Infer.expect(params)
    @Infer.doc(responses={200: 'Success'})
    @Infer.doc(responses={420: 'Your Source Path Not Found'})
    @Infer.doc(responses={421: 'Your Target Path Not Found'})
    def post(self):
        start = time.time()
        logging.info(f"Face Swap Start")
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {"message": "Please Login"}, 409

        source_path = request.json['source']
        target_path = request.json['target']
        logging.info(f"source_path: {source_path} target_path: {target_path}")
        if not os.path.isfile(source_path):
            logging.error("message : Your Source Path Not Found")
            return {
                "message" : "Your Source Path Not Found"
                }, 420
        elif not os.path.isfile(target_path):
            logging.error("message : Your Target Path Not Found")
            return {
                "message" : "Your Target Path Not Found"
                }, 421
        result_file = core.cli(source_path, target_path, face_enhancer_mode="face_enhancer")
        logging.info(f"end time: {time.time()-start:.4f} sec")
        print(f"end time: {time.time()-start:.4f} sec")

        output_file = os.path.isfile(result_file)
        if output_file:
            result=dict(
                status="Image Create success"
            )
        else:
            result=dict(
                status="Not Image FaceFusion"
            )
        return result["status"]