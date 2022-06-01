const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');

const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
  selfieMode:true,  //canvasを反転
  maxNumHands: 2,
  modelComplexity: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
hands.onResults(getHand);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await hands.send({image: videoElement});
  },
  width: 540,
  height: 320
});
camera.start();

function getHand(results) {
  canvasCtx.save();
  //canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,{color: '#02c8a7', lineWidth: 4});
      drawLandmarks(canvasCtx, landmarks, {color: '#f9be02', lineWidth: 0.05});
      //landmark = landmarks;
      //console.log(landmarks[8]);
      
      let oyaX = landmarks[4].x;
      let oyaY = landmarks[4].y;
      let hitoX = landmarks[8].x;
      let hitoY = landmarks[8].y;
      let nakaX = landmarks[12].x;
      let nakaY = landmarks[12].y;
      let kusuX = landmarks[16].x;
      let kusuY = landmarks[16].y;
      let koX = landmarks[20].x;
      let koY = landmarks[20].y;

      if(Math.abs(oyaX - hitoX) < 0.02 && Math.abs(oyaY - hitoY) < 0.027){
        console.log("👌");
        //alert("👌");
        } else if(nakaY > landmarks[17].y && kusuY > landmarks[17].y){
          //console.log("📷");
        }
      }
  }
  canvasCtx.restore();
}
