import {request,post} from './client';
import type {Report} from '../types/domain';
export const listReports=()=>request<Report[]>('/reports');
export const createReports=(data:unknown)=>post<Report>('/reports',data);
