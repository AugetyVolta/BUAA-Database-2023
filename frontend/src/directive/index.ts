export default class Directive {
  constructor() { }
  watermark(app: any): void {
    app.directive("watermark", {
      beforeMount(el: any, binding: any) {
        const watermarkText: any = binding.value || '星域'; // 水印文本，默认为"星域"
        const canvas: any = document.createElement('canvas');
        const ctx: any = canvas.getContext('2d');
        canvas.width = 200; // 设置canvas的宽度
        canvas.height = 150; // 设置canvas的高度
        ctx.font = '16px Arial'; // 设置水印文本的字体样式和大小
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)'; // 设置水印文本的颜色和透明度
        ctx.rotate(-Math.PI / 4); // 设置水印文本的旋转角度
        ctx.fillText(watermarkText, -canvas.height / 2, canvas.width / 2); // 绘制水印文本
        el.style.backgroundImage = `url(${canvas.toDataURL()})`; // 将canvas转为图片URL，并设置为元素的背景图
      }
    });
  }
  // demo(app: any): void {
  //   app.directive("demo", {
  //     beforeMount(el: any, binding: any) {
  //       console.log(el);
  //       console.log(binding);

  //     }
  //   })
  // }
}

