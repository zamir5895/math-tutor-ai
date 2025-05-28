import React, { useState, useEffect } from 'react'
import { Ear, Mic, Glasses } from 'lucide-react'
import MateMixBar from '../LogoBar/MateMixBar'
import logoMateMix from '../../assets/MateMix_Logo.png'
import ImagenPuercoEspin from '../../assets/AVATAR-PUERCOESPIN.png'

const StudentDashboardComponent = () => {
  return (
    <div className="p-6 font-sans bg-white min-h-screen">
      <header className="flex items-center border-b-[1px] border-gray-300 pb-3 mb-6">
        <img src={logoMateMix} alt="MateMix Logo" className="h-10" />
      </header>

      <div className="flex flex-col gap-6">
        <div className="flex gap-8 items-start">
            <div className="relative ml-20 w-57 h-48 bg-[#10B981] flex items-center justify-center rounded-full">
            <div className="absolute w-25 h-25 bg-white rounded-full flex items-center justify-center">
        <img src={ImagenPuercoEspin} alt="Icono" className="w-18 h-18" />
        </div>
          </div>
          <div className="flex-1 ml-20">
            <p className="text-lg mb-8 leading-relaxed">
              <span className="font-bold">Estudiante:</span>
              <span className="font-bold ml-10">Aguinaga Pizarro, Bianca Brunella</span>
            </p>
            <div className="flex gap-16">
              <p className="font-bold">Aprendizaje:</p>
              <div className="space-y-6">
                <div className="flex items-center gap-3">
                  <Glasses className="w-5 h-5" />
                  <span className="w-16 text-sm font-bold">Visual</span>
                  <span className="font-bold text-sm">10%</span>
                  <div className="w-64 h-4 bg-gray-200 rounded-full border border-black">
                    <div className="h-full bg-[#10B981] rounded-full border border-black" style={{width: '10%'}}></div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Ear className="w-5 h-5" />
                  <span className="w-16 text-sm font-bold">Auditivo</span>
                  <span className="font-bold text-sm">30%</span>
                  <div className="w-64 h-4 bg-gray-200 rounded-full border border-black">
                    <div className="h-full bg-[#D8315B] rounded-full border border-black" style={{width: '30%'}}></div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Mic className="w-5 h-5" />
                  <span className="w-16 text-sm font-bold">Verbal</span>
                  <span className="font-bold text-sm">60%</span>
                  <div className="w-64 h-4 bg-gray-200 rounded-full border border-black">
                    <div className="h-full bg-[#FFA000] rounded-full border border-black" style={{width: '60%'}}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mt-6">
          <div className="bg-gray-200 h-48 rounded-lg"></div>
          <div className="bg-gray-200 h-48 rounded-lg"></div>
        </div>
      </div>
    </div>
  )
}

export default StudentDashboardComponent
