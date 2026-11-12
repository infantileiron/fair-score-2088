import {request,post} from './client';
import type {Review} from '../types/domain';
export const listReviews=()=>request<Review[]>('/reviews');
export const createReviews=(data:unknown)=>post<Review>('/reviews',data);
