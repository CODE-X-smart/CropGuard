import React, { useState } from 'react';
import Navbar from './components/Navbar';
import StageAAlertBanner from './components/StageAAlertBanner';
import ImageDiagnosisCard from './components/ImageDiagnosisCard';
import FusionResultCard from './components/FusionResultCard';
import TreatmentAdvisory from './components/TreatmentAdvisory';
import AdminDashboard from './components/AdminDashboard';
import { translations } from './i18n/translations';

export default function App() {
  const [activeTab, setActiveTab] = useState('farmer');
  const [lang, setLang] = useState('en');
  const [crop, setCrop] = useState('Tomato');
  const [district, setDistrict] = useState('Nashik');
  const [diagnosis, setDiagnosis] = useState(null);
  const [stageAResult, setStageAResult] = useState(null);

  const t = translations[lang] || translations.en;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-emerald-600 selection:text-white">
      {/* Navigation Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        lang={lang}
        setLang={setLang}
        t={t}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'farmer' ? (
          <div>
            {/* Stage A Pre-Symptomatic Risk Alert Banner */}
            <StageAAlertBanner
              crop={crop}
              setCrop={setCrop}
              district={district}
              setDistrict={setDistrict}
              t={t}
              onStageAPredicted={(res) => setStageAResult(res)}
            />

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Left Column: Image Upload Card */}
              <div className="lg:col-span-6">
                <ImageDiagnosisCard
                  crop={crop}
                  district={district}
                  t={t}
                  onDiagnosisComplete={(res) => setDiagnosis(res)}
                />
              </div>

              {/* Right Column: Diagnostic Fusion & Treatment Advisory */}
              <div className="lg:col-span-6">
                {diagnosis ? (
                  <div>
                    <FusionResultCard diagnosis={diagnosis} t={t} />
                    <TreatmentAdvisory advisory={diagnosis.treatment_advisory} t={t} />
                  </div>
                ) : (
                  <div className="bg-white rounded-xl p-8 text-center border-2 border-dashed border-slate-200 shadow-xs">
                    <div className="w-14 h-14 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-3 text-emerald-700 text-xl">
                      🌿
                    </div>
                    <h3 className="text-base font-bold text-slate-800">Awaiting Leaf Diagnosis</h3>
                    <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto leading-relaxed">
                      Upload a leaf photo on the left or select one of the sample images to generate a comprehensive Stage A + B diagnostic advisory.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <AdminDashboard t={t} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-500 mt-12 shadow-xs">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span className="font-medium text-slate-600">© 2026 CropGuard AI — Precision Agriculture Advisory System</span>
          <span className="text-emerald-700 font-medium text-[11px] bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
            PyTorch MobileNetV3 Vision & Epidemiological Forecasting Engine
          </span>
        </div>
      </footer>
    </div>
  );
}
