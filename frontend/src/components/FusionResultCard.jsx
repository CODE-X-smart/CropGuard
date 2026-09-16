import React from 'react';
import { ShieldCheck, Activity, Eye, Percent, Info, AlertOctagon } from 'lucide-react';

export default function FusionResultCard({ diagnosis, t }) {
  if (!diagnosis) return null;

  const { fusion, stage_b, treatment_advisory } = diagnosis;
  const isHealthy = fusion.disease_id === 'Healthy_Leaf';

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 mb-8 shadow-xs">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200 pb-4 mb-6">
        <div>
          <span className="text-[11px] font-bold px-2.5 py-1 rounded bg-emerald-50 text-emerald-800 border border-emerald-200 uppercase tracking-wider">
            {t.fusionTitle}
          </span>
          <h2 className="text-xl md:text-2xl font-bold text-slate-900 mt-2 flex items-center gap-2">
            {fusion.disease_name}
            {isHealthy && <span className="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-200">CLEAN FOLIAGE</span>}
          </h2>
          {treatment_advisory?.scientific_name && treatment_advisory.scientific_name !== 'N/A' && (
            <p className="text-xs text-emerald-700 font-medium italic mt-0.5">
              Pathogen: {treatment_advisory.scientific_name}
            </p>
          )}
        </div>

        {/* Unified Fusion Confidence Score Badge */}
        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 text-center min-w-[140px] shadow-xs">
          <span className="text-[11px] font-semibold text-slate-500 block">{t.fusionScoreLabel}</span>
          <span className="text-3xl font-black text-emerald-700">
            {fusion.fusion_confidence_pct}%
          </span>
        </div>
      </div>

      {/* Metrics Breakdown Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div className="flex items-center justify-between text-xs text-slate-600 mb-1.5">
            <span className="flex items-center gap-1.5 font-medium"><Activity className="w-3.5 h-3.5 text-indigo-600" /> {t.stageARiskLabel}</span>
            <span className="font-bold text-slate-900">{fusion.stage_a_risk_pct}%</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div className="bg-indigo-600 h-full rounded-full" style={{ width: `${fusion.stage_a_risk_pct}%` }}></div>
          </div>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div className="flex items-center justify-between text-xs text-slate-600 mb-1.5">
            <span className="flex items-center gap-1.5 font-medium"><Eye className="w-3.5 h-3.5 text-teal-600" /> {t.stageBConfLabel}</span>
            <span className="font-bold text-slate-900">{fusion.stage_b_confidence_pct}%</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div className="bg-teal-600 h-full rounded-full" style={{ width: `${fusion.stage_b_confidence_pct}%` }}></div>
          </div>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div className="flex items-center justify-between text-xs text-slate-600 mb-1.5">
            <span className="flex items-center gap-1.5 font-medium"><Percent className="w-3.5 h-3.5 text-amber-600" /> {t.severityLabel}</span>
            <span className="font-bold text-amber-700">{fusion.severity_pct}%</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div className="bg-amber-600 h-full rounded-full" style={{ width: `${Math.min(100, fusion.severity_pct * 2)}%` }}></div>
          </div>
          <span className="text-[10px] text-slate-500 block mt-1 font-medium">{fusion.severity_grade}</span>
        </div>
      </div>

      {/* Visual Explanation Box */}
      <div className="bg-emerald-50/70 p-4 rounded-xl border border-emerald-200 mb-2">
        <h4 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-1 flex items-center gap-1.5">
          <Info className="w-4 h-4 text-emerald-700" /> {t.detectedFeaturesTitle}
        </h4>
        <p className="text-xs text-slate-800 leading-relaxed">
          {fusion.confidence_weighted_explanation}
        </p>
        {treatment_advisory?.key_visual_features && (
          <p className="text-xs text-slate-700 mt-2 pt-2 border-t border-emerald-200/80">
            <strong className="text-slate-900">ICAR Feature Pattern:</strong> {treatment_advisory.key_visual_features}
          </p>
        )}
      </div>
    </div>
  );
}
