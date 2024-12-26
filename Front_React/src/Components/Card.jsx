import React from 'react';

export function PerfumeCard({ image, name, price, marca }) {
  return (
    <div className="max-w-xs border rounded-lg shadow-md overflow-hidden">
      <img src={image} alt={name} className="w-full h-48 object-cover" />
      <div className="p-4 text-center">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">{marca}</h2>
        <h3 className="text-gray-600 text-sm">{name}</h3>
        <p className="text-green-600 text-xl font-bold mb-2">${price}</p>
      </div>
    </div>
  );
}

export default PerfumeCard;

// Ejemplo de uso
// <PerfumeCard 
//   image="https://example.com/perfume.jpg" 
//   name="Eau de Parfum" 
//   price={120.99} 
//   season="Primavera y Verano" 
// />

