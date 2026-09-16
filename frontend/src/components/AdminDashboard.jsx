import React, { useState, useEffect } from 'react';
import { MapPin, Filter, AlertCircle, CheckCircle2, ShieldAlert, BarChart3, Database } from 'lucide-react';
import { api } from '../api/client';

export default function AdminDashboard({ t }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cropFilter, setCropFilter] = useState('ALL');
  const [riskFilter, setRiskFilter] = useState('ALL');

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const res = await api.getDashboardData(cropFilter, riskFilter);
      setData(res);
    } catch (err) {
      console.error("Dashboard fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [cropFilter, riskFilter]);

  if (loading && !data) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-500 shadow-xs">
        <Database className="w-8 h-8 animate-spin mx-auto mb-2 text-emerald-700" />
        <p className="text-xs font-medium">Loading District Risk Heatmap & Clustering Engine...</p>
      </div>
    );
  }

  const { summary, district_heatmap, recent_diagnoses } = data || {
    summary: { total_districts_monitored: 0, high_risk_clusters: 0, moderate_risk_clusters: 0, low_risk_clusters: 0 },
    district_heatmap: [],
    recent_diagnoses: []
  };

  return (
    <div className="space-y-6">
      {/* Dashboard Title */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xs">
        <div>
          <span className="text-[11px] font-bold px-2.5 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-200 uppercase tracking-wider">
            EXTENSION OFFICER PORTAL
          </span>
          <h2 className="text-xl md:text-2xl font-bold text-slate-900 mt-1">
            {t.dashTitle}
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">{t.dashSub}</p>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div>
            <label className="text-[10px] font-semibold text-slate-600 block mb-1">{t.filterCrop}</label>
            <select
              value={cropFilter}
              onChange={(e) => setCropFilter(e.target.value)}
              className="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 shadow-xs"
            >
              <option value="ALL">{t.allCrops}</option>
              <option value="Tomato">Tomato</option>
              <option value="Potato">Potato</option>
              <option value="Corn/Maize">Corn/Maize</option>
            </select>
          </div>

          <div>
            <label className="text-[10px] font-semibold text-slate-600 block mb-1">{t.filterRisk}</label>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-600 shadow-xs"
            >
              <option value="ALL">{t.allRisks}</option>
              <option value="HIGH">High Risk</option>
              <option value="MODERATE">Moderate Risk</option>
              <option value="LOW">Low Risk</option>
            </select>
          </div>
        </div>
      </div>

      {/* Cluster Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 block">{t.monitoredDistricts}</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">{summary.total_districts_monitored}</span>
          <span className="text-[10px] text-emerald-700 font-medium block mt-1">Active Automated Sensing</span>
        </div>

        <div className="bg-rose-50/70 rounded-xl p-4 border border-rose-200 shadow-xs">
          <span className="text-xs font-semibold text-rose-900 block">{t.highRiskClusters}</span>
          <span className="text-2xl font-black text-rose-700 mt-1 block">{summary.high_risk_clusters}</span>
          <span className="text-[10px] text-rose-700 font-medium block mt-1">Immediate Alert Action Required</span>
        </div>

        <div className="bg-amber-50/70 rounded-xl p-4 border border-amber-200 shadow-xs">
          <span className="text-xs font-semibold text-amber-900 block">{t.modRiskClusters}</span>
          <span className="text-2xl font-black text-amber-700 mt-1 block">{summary.moderate_risk_clusters}</span>
          <span className="text-[10px] text-amber-800 font-medium block mt-1">Heightened Surveillance</span>
        </div>

        <div className="bg-emerald-50/70 rounded-xl p-4 border border-emerald-200 shadow-xs">
          <span className="text-xs font-semibold text-emerald-900 block">{t.lowRiskClusters}</span>
          <span className="text-2xl font-black text-emerald-700 mt-1 block">{summary.low_risk_clusters}</span>
          <span className="text-[10px] text-emerald-800 font-medium block mt-1">Normal Agricultural Status</span>
        </div>
      </div>

      {/* District Outbreak Heatmap Grid */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 shadow-xs">
        <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
          <MapPin className="w-4 h-4 text-emerald-700" />
          District Outbreak Risk Grid (Stage-A Epidemiological Predictions)
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {district_heatmap.map((d) => (
            <div
              key={d.id}
              className={`p-4 rounded-xl border transition-all ${
                d.alert_level === 'HIGH'
                  ? 'bg-rose-50/60 border-rose-200 hover:border-rose-300'
                  : d.alert_level === 'MODERATE'
                  ? 'bg-amber-50/60 border-amber-200 hover:border-amber-300'
                  : 'bg-emerald-50/50 border-emerald-200 hover:border-emerald-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div>
                  <h4 className="text-sm font-bold text-slate-900">{d.district_name}</h4>
                  <span className="text-[10px] text-slate-500 font-medium">{d.state} • {d.crop_type}</span>
                </div>
                <span className={`px-2 py-0.5 text-[10px] font-bold rounded uppercase ${
                  d.alert_level === 'HIGH' ? 'bg-rose-600 text-white' : d.alert_level === 'MODERATE' ? 'bg-amber-600 text-white' : 'bg-emerald-700 text-white'
                }`}>
                  {d.alert_level}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs my-2 pt-2 border-t border-slate-200">
                <span className="text-slate-600">Risk Score:</span>
                <span className="font-extrabold text-slate-900">{d.risk_score}%</span>
              </div>

              <div className="text-[11px] text-slate-800">
                <span className="text-slate-500">Threat: </span>
                <span className="font-bold text-amber-900">{d.primary_threat}</span>
              </div>

              <div className="mt-2 text-[10px] text-slate-500 flex items-center justify-between pt-2 border-t border-slate-200/80">
                <span>Temp: {d.temperature}°C | RH: {d.humidity}%</span>
                <span>LWD: {d.leaf_wetness_hours}h</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Farmer Diagnoses Log Table */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 md:p-6 overflow-hidden shadow-xs">
        <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-teal-700" />
          {t.recentReports}
        </h3>

        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-100 text-slate-700 border-b border-slate-200 uppercase text-[10px] tracking-wider font-semibold">
              <tr>
                <th className="py-3 px-4">{t.colDistrict}</th>
                <th className="py-3 px-4">{t.colCrop}</th>
                <th className="py-3 px-4">{t.colDisease}</th>
                <th className="py-3 px-4">{t.colSeverity}</th>
                <th className="py-3 px-4">{t.colRisk}</th>
                <th className="py-3 px-4">{t.colConf}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white">
              {recent_diagnoses.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4 font-semibold text-slate-900">{r.district_name}, {r.state}</td>
                  <td className="py-3 px-4">{r.crop_type}</td>
                  <td className="py-3 px-4 text-emerald-800 font-semibold">{r.disease_predicted.replace(/_/g, ' ')}</td>
                  <td className="py-3 px-4 font-bold text-amber-700">{r.severity_pct}%</td>
                  <td className="py-3 px-4 text-indigo-700 font-medium">{r.stage_a_risk}%</td>
                  <td className="py-3 px-4 font-black text-teal-800">{r.fusion_confidence}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
