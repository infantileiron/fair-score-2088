export const percent=(v:number|null|undefined)=>v==null?'无分母':(v*100).toFixed(1)+'%';
export const comparison=(v:number|null|undefined)=>v==null?'不可比较':percent(v);
export const weight=(v:number)=>Number(v.toFixed(6)).toString();
export const date=(v:string)=>new Date(v).toLocaleString('zh-CN',{hour12:false});
export const short=(v:string)=>v.length>12?v.slice(0,12)+'…':v;
