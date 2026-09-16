import React from 'react';
import { Leaf, Globe, LayoutDashboard, Stethoscope } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, lang, setLang, t }) {
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Brand logo & title */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-700 flex items-center justify-center shadow-xs">
            <Leaf className="w-5 h-5 text-white stroke-[2.2]" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-xl font-bold text-slate-900 tracking-tight">
                {t.title}
              </h1>
              <span className="px-2 py-0.5 text-[11px] font-semibold rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
                Official Advisory
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">
              {t.tagline}
            </p>
          </div>
        </div>

        {/* Navigation tabs & Language switch */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end">
          <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200">
            <button
              onClick={() => setActiveTab('farmer')}
              className={`flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-md transition-all ${
                activeTab === 'farmer'
                  ? 'bg-emerald-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <Stethoscope className="w-3.5 h-3.5" />
              {t.navFarmer}
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-md transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-emerald-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              {t.navDashboard}
            </button>
          </div>

          <button
            onClick={() => setLang(lang === 'en' ? 'hi' : 'en')}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200/80 transition-all shadow-xs"
            title="Toggle Language / भाषा बदलें"
          >
            <Globe className="w-3.5 h-3.5 text-amber-700" />
            {t.langToggle}
          </button>
        </div>
      </div>
    </header>
  );
}

