import type {User} from '../types/domain';
export function readUser():User|null{try{return JSON.parse(localStorage.getItem('fair-user')||'null')}catch{return null}}
export function saveSession(token:string,user:User){localStorage.setItem('fair-token',token);localStorage.setItem('fair-user',JSON.stringify(user))}
export function clearSession(){localStorage.removeItem('fair-token');localStorage.removeItem('fair-user')}
