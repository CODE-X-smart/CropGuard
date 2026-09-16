import React, { useState, useEffect } from 'react';
import { AlertTriangle, Thermometer, Droplets, CloudRain, Clock, Sparkles, Activity } from 'lucide-react';
import { api } from '../api/client';

export default function StageAAlertBanner({ crop, setCrop, district, setDistrict, t, onStageAPredicted }) {
  const [growthStage, setGrowthStage] = useState('Flowering');
  const [temperature, setTemperature] = useState(21.5);
  const [humidity, setHumidity] = useState(88.0);
  const [rainfall, setRainfall] = useState(12.0);
  const [leafWetness, setLeafWetness] = useState(11.5);
  const [loading, setLoading] = useState(false);
  const [stageAResult, setStageAResult] = useState(null);

  const handlePredictRisk = async () => {
    setLoading(true);
    try {
      const data = await api.predictRisk({
        crop_type: crop,
        growth_stage: growthStage,
        district: district,
        temperature: parseFloat(temperature),
        humidity: parseFloat(humidity),
        rainfall_mm: parseFloat(rainfall),
        leaf_wetness_hours: parseFloat(leafWetness)
      });
      setStageAResult(data);
      if (onStageAPredicted) onStageAPredicted(data);
    } catch (err) {
      console.error("Stage A prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handlePredictRisk();
  }, [crop, district]);

  const alertClass = stageAResult?.alert_level === 'HIGH'
    ? 'bg-rose-50/80 border-rose-300 text-rose-950 high-risk-alert-pulse'
    : stageAResult?.alert_level === 'MODERATE'
    ? 'bg-amber-50/80 border-amber-300 text-amber-950'
    : 'bg-emerald-50/80 border-emerald-300 text-emerald-950';

  return (
    <div className={`rounded-xl border p-5 md:p-6 mb-8 transition-all shadow-xs ${alertClass}`}>
      {/* Header Banner Title */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-5 border-b border-slate-200/80 pb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-lg ${
            stageAResult?.alert_level === 'HIGH'
              ? 'bg-rose-100 text-rose-700 border border-rose-200'
              : stageAResult?.alert_level === 'MODERATE'
              ? 'bg-amber-100 text-amber-800 border border-amber-200'
              : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
          }`}>
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 border border-indigo-200">
                PRE-SYMPTOMATIC STAGE-A
              </span>
              <h2 className="text-lg md:text-xl font-bold text-slate-900">
                {t.stageATitle}
              </h2>
            </div>
            <p className="text-xs text-slate-600 mt-0.5">
              {t.stageASub}
            </p>
          </div>
        </div>

        {stageAResult && (
          <div className="flex items-center gap-3 self-end sm:self-auto">
            <div className="text-right">
              <span className="text-xs font-semibold text-slate-500 block">{t.riskScoreText}</span>
              <span className={`text-2xl font-black ${
                stageAResult.alert_level === 'HIGH' ? 'text-rose-700' : stageAResult.alert_level === 'MODERATE' ? 'text-amber-700' : 'text-emerald-700'
              }`}>
                {stageAResult.stage_a_risk_score}%
              </span>
            </div>
            <span className={`px-3 py-1.5 text-xs font-bold rounded-md uppercase tracking-wider shadow-xs ${
              stageAResult.alert_level === 'HIGH'
                ? 'bg-rose-600 text-white'
                : stageAResult.alert_level === 'MODERATE'
                ? 'bg-amber-600 text-white'
                : 'bg-emerald-700 text-white'
            }`}>
              {stageAResult.alert_level}
            </span>
          </div>
        )}
      </div>

      {/* Dynamic Weather & Crop Controls */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-4">
        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 block">{t.districtLabel}</label>
          <select
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          >
            <option value="Nashik">Nashik (MH)</option>
            <option value="Karnal">Karnal (HR)</option>
            <option value="Ludhiana">Ludhiana (PB)</option>
            <option value="Anand">Anand (GJ)</option>
            <option value="Guntur">Guntur (AP)</option>
            <option value="Shimla">Shimla (HP)</option>
            <option value="Varanasi">Varanasi (UP)</option>
          </select>
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 block">{t.cropLabel}</label>
          <select
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          >
            <option value="Tomato">Tomato</option>
            <option value="Potato">Potato</option>
            <option value="Corn/Maize">Corn / Maize</option>
          </select>
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 block">{t.growthStageLabel}</label>
          <select
            value={growthStage}
            onChange={(e) => setGrowthStage(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          >
            <option value="Seedling">Seedling</option>
            <option value="Vegetative">Vegetative</option>
            <option value="Flowering">Flowering</option>
            <option value="Fruiting">Fruiting</option>
          </select>
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1">
            <Thermometer className="w-3.5 h-3.5 text-amber-600" /> {t.tempLabel}
          </label>
          <input
            type="number"
            step="0.5"
            value={temperature}
            onChange={(e) => setTemperature(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          />
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1">
            <Droplets className="w-3.5 h-3.5 text-teal-600" /> {t.humidityLabel}
          </label>
          <input
            type="number"
            step="1"
            value={humidity}
            onChange={(e) => setHumidity(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          />
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-indigo-600" /> {t.leafWetnessLabel}
          </label>
          <input
            type="number"
            step="0.5"
            value={leafWetness}
            onChange={(e) => setLeafWetness(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 shadow-xs"
          />
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
        <button
          onClick={handlePredictRisk}
          disabled={loading}
          className="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2 text-xs font-bold rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white transition-all shadow-xs"
        >
          <Activity className="w-4 h-4" />
          {loading ? 'Computing...' : t.predictRiskBtn}
        </button>

        {stageAResult && (
          <div className="text-xs text-slate-800 bg-white/90 p-2.5 rounded-lg border border-slate-200 w-full sm:w-auto flex-1 shadow-xs">
            <span className="font-bold text-amber-800">Predicted Threat: {stageAResult.primary_threat}</span> — {stageAResult.reasoning}
          </div>
        )}
      </div>
    </div>
  );
}
