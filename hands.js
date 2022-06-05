const videoElement = document.getElementsByClassName('input_video')[0];
videoElement.style.display = "none";
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');

var img_src = new Array("image/maloik_sign_sdw.png","image/maloik_sign1.png","image/ok_sign_sdw.png","image/ok_sign1.png","image/kitune_sdw.png","image/kitune1.png");
let i = 0;
let isGestureDetected = false;  // ジェスチャーを検出したかのフラグ

const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
  selfieMode:true,  //canvasを反転
  maxNumHands: 2,
  modelComplexity: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.8
});
hands.onResults(getHand);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await hands.send({image: videoElement});
  },
  width: 768,
  height: 432
});
camera.start();

const onGestureDetected = () => {
  isGestureDetected = true;
  setTimeout(() => {
    isGestureDetected = false;
  }, 1000);
};

function getHand(results) {
  canvasCtx.save();
  //canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,{color: '#02c8a7', lineWidth: 4});
      drawLandmarks(canvasCtx, landmarks, {color: '#f9be02', lineWidth: 0.05});
      //landmark = landmarks;
      //console.log(results.multiHandLandmarks[0]);
      const hand  = results.multiHandLandmarks;
      const hand1 = results.multiHandLandmarks[0] ;
      const hand2 = results.multiHandLandmarks[1];
      //console.log(hand);
/*
      if (!isGestureDetected && (hand1[6].y < hand1[8].y > hand1[7].y) && (hand1[10].y < hand1[12].y > hand1[11].y) && (0.02 < Math.abs(hand1[8].x - hand1[12].x) > 0.07)) {
        function counter(){
          i++;
          document.getElementById("press-button").innerHTML = i;
        }
        counter();
        console.log("✌🏻");
        onGestureDetected();
      }
*/
      if (!isGestureDetected && (hand1[12].y > hand1[10].y) && (hand1[16].y > hand1[14].y) && (hand1[8].y < hand1[10].y) && (hand1[20].y < hand1[10].y) && (hand1[4].y < hand1[11].y)) {
        function change(){
          document.getElementById("img1").src=img_src[1];
        }
        change();
        //console.log("🤘");
        //onGestureDetected();
      } else{
        document.getElementById("img1").src=img_src[0];
      }

      if (!isGestureDetected && Math.abs(hand1[4].x - hand1[8].x) < 0.03 && Math.abs(hand1[4].y - hand1[8].y) < 0.03){
        function change(){
          document.getElementById("img2").src=img_src[3];
        }
        change();
        //console.log("👌");
        //onGestureDetected();
      } else{
        document.getElementById("img2").src=img_src[2];
      }

      if (!isGestureDetected && Math.abs(hand1[4].x - hand1[12].x) < 0.05 && Math.abs(hand1[4].y - hand1[12].y) < 0.05 && Math.abs(hand1[4].x - hand1[16].x) < 0.05 && Math.abs(hand1[4].y - hand1[16].y) < 0.05){
        function change(){
          document.getElementById("img3").src=img_src[5];
        }
        change();
        //console.log("🤟");
        //onGestureDetected();
      } else{
        document.getElementById("img3").src=img_src[4];
      }
      /*
      if ((hand1[6].y < hand1[8].y > hand1[7].y) && (hand1[10].y < hand1[12].y > hand1[11].y) && (0.03 < Math.abs(hand1[8].x - hand1[12].x) > 0.07) && i == 0) {
        i = 1;
        console.log("👌",i);
        //location.href ='test/demo用.html';
        //alert("👌");
      }

      if(0.03 < Math.abs(hand1[8].x - hand1[12].x) > 0.065){
        console.log("👌");
        //location.href ='test/demo用.html';
        //alert("👌");
      }
      */
    //canvasCtx.restore();

    }
  }
}
