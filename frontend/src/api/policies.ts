import {request,post} from './client';
import type {Policy} from '../types/domain';
export const listPolicies=()=>request<Policy[]>('/policies');
export const createPolicies=(data:unknown)=>post<Policy>('/policies',data);
