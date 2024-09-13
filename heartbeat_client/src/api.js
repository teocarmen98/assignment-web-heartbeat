import axios from "axios";

const API_URL = 'http://10.128.1.129/api';

export const getMainListing = (params) => {
    return axios.get(`${API_URL}/urls/`, { params });
}
export const getDetail = (id) => {
    return axios.get(`${API_URL}/urls/${id}`);
}
export const createDetail = (data) => {
    return axios.post(`${API_URL}/urls/`, data);
}
export const updateDetail = (id, data) => {
    return axios.put(`${API_URL}/urls/${id}`, data);
}
export const deleteDetail = (id) => {
    return axios.delete(`${API_URL}/urls/${id}`);
}