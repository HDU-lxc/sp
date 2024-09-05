window = global;
delete global;
delete Buffer;

window.requestAnimationFrame = function () {}
document = {}
// screen = {
//     availHeight: 1112,
//     availLeft: 0,
//     availTop: 0,
//     availWidth: 2048,
//     colorDepth: 24,
//     height: 1152
// }
window.screen = {
    availWidth: 1920,
    availHeight: 1032,
    width: 1920,
    height: 1080,
    colorDepth: 24,
    pixelDepth: 24,
    orientation: {
        type: "landscape-primary",
        angle: 0
    },
};


window.innerWidth = 1920
window.innerHeight = 1080
window.outerWidth = 1914
// window.outerHeight = 1026
// window.screenX = 2563
// window.screenY = 412




navigator = {}


XMLHttpRequest = function () {}

// function setProxy(proxyObjs) {
//     for (let i = 0; i < proxyObjs.length; i++) {
//         const handler = `{
//       get: function(target, property, receiver) {
//        if (property != "Math" && property != "isNaN") {
//             if (target[property] && typeof target[property] != 'string' && Object.keys(target[property]).length > 3) {
//             } else {
//             console.log("方法:", "get  ", "对象:", "${proxyObjs[i]}", "  属性:", property, "  属性类型：", typeof property, ", 属性值：", target[property], ", 属性值类型：", typeof target[property]);}}
//             return target[property];
//       },
//       set: function(target, property, value, receiver) {
//         console.log("方法:", "set  ", "对象:", "${proxyObjs[i]}", "  属性:", property, "  属性类型：", typeof property, ", 属性值：", value, ", 属性值类型：", typeof target[property]);
//         return Reflect.set(...arguments);
//       }
//     }`;
//         eval(`try {
//             ${proxyObjs[i]};
//             ${proxyObjs[i]} = new Proxy(${proxyObjs[i]}, ${handler});
//         } catch (e) {
//             ${proxyObjs[i]} = {};
//             ${proxyObjs[i]} = new Proxy(${proxyObjs[i]}, ${handler});
//         }`);
//     }
// }
//
// setProxy(['window'])


