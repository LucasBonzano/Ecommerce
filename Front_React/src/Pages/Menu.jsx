import React from 'react'
import { PerfumeCard } from '../Components/Card'

export function Menu() {
  return (
    <div className='grid grid-cols-3 justify-center'>
      <PerfumeCard image="https://perfumeshop.com.ar/wp-content/uploads/2024/09/Mandarin-sky-2.webp" name="Odyssey Mandarin Sky" price={120.99} marca="Armaf" />
      <PerfumeCard image="https://perfumeshop.com.ar/wp-content/uploads/2024/09/Mandarin-sky-2.webp" name="Odyssey Mandarin Sky" price={120.99} marca="Armaf" />
      <PerfumeCard image="https://perfumeshop.com.ar/wp-content/uploads/2024/09/Mandarin-sky-2.webp" name="Odyssey Mandarin Sky" price={120.99} marca="Armaf" />
      <PerfumeCard image="https://perfumeshop.com.ar/wp-content/uploads/2024/09/Mandarin-sky-2.webp" name="Odyssey Mandarin Sky" price={120.99} marca="Armaf" />

    </div>
  )
}
