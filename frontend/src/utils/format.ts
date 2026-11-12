export const percent=(v:number|null|undefined)=>v==null?'无分母':(v*100).toFixed(1)+'%';
export const date=(v:string)=>new Date(v).toLocaleString('zh-CN',{hour12:false});
export const short=(v:string)=>v.length>12?v.slice(0,12)+'…':v;
