import {request,post} from './client';
import type {Run} from '../types/domain';
export const listRuns=()=>request<Run[]>('/runs');
export const createRuns=(data:unknown)=>post<Run>('/runs',data);
