import {request,post} from './client';
import type {Dataset} from '../types/domain';
export const listDatasets=()=>request<Dataset[]>('/datasets');
export const createDatasets=(data:unknown)=>post<Dataset>('/datasets',data);
