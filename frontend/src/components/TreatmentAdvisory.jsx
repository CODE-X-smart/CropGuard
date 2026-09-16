import React from 'react';
import { Sprout, ShieldAlert, AlertTriangle, FileText, Check } from 'lucide-react';

export default function TreatmentAdvisory({ advisory, t }) {
  if (!advisory) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 mb-8 shadow-xs">
      <div className="flex items-center gap-3 mb-5 border-b border-slate-200 pb-3">
        <div className="p-2 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
          <Sprout className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900">{t.treatmentTitle}</h3>
          <p className="text-xs text-slate-500">Integrated Pest & Disease Management Guidelines</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Organic Options */}
        <div className="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="p-1 rounded bg-emerald-100 text-emerald-800">
              <Check className="w-4 h-4" />
            </span>
            <h4 className="text-sm font-bold text-emerald-900">{t.organicTitle}</h4>
          </div>
          <p className="text-xs text-slate-800 leading-relaxed">
            {advisory.organic_treatment}
          </p>
        </div>

        {/* Chemical Options */}
        <div className="bg-amber-50/70 p-4 rounded-xl border border-amber-200">
          <div className="flex items-center gap-2 mb-2">
            <span className="p-1 rounded bg-amber-100 text-amber-800">
              <FileText className="w-4 h-4" />
            </span>
            <h4 className="text-sm font-bold text-amber-950">{t.chemicalTitle}</h4>
          </div>
          <p className="text-xs text-slate-800 leading-relaxed">
            {advisory.chemical_treatment}
          </p>
        </div>
      </div>

      {/* Required Dosage Caveat Disclaimer */}
      <div className="bg-rose-50/80 p-4 rounded-xl border border-rose-200 flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-rose-700 shrink-0 mt-0.5" />
        <div>
          <h5 className="text-xs font-bold text-rose-900 uppercase tracking-wider mb-1">
            {t.disclaimerTitle}
          </h5>
          <p className="text-xs text-slate-700 leading-relaxed">
            {t.disclaimerText}
          </p>
        </div>
      </div>
    </div>
  );
}
