// src/components/AnalisisList.js
import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosConfig';

const AnalisisList = () => {
    const [analisis, setAnalisis] = useState([]);

    useEffect(() => {
        axiosInstance.get('analisis/')
            .then(response => {
                setAnalisis(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    return (
        <div>
            <h1>Lista de Análisis</h1>
            <ul>
                {analisis.map(item => (
                    <li key={item.id_analisis}>{item.titulo_descriptivo}</li>
                ))}
            </ul>
        </div>
    );
};

export default AnalisisList;
