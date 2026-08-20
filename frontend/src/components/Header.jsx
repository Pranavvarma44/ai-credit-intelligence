import { ShieldCheck, Activity } from "lucide-react";

function Header() {
  return (
    <header className="border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-18 max-w-6xl items-center justify-between px-6 lg:px-8">

        {/* Brand */}
        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-900 text-white shadow-sm">
            <ShieldCheck size={21} />
          </div>

          <div>
            <h1 className="text-[17px] font-bold tracking-tight text-slate-900">
              CreditRisk
            </h1>

            <p className="text-[11px] text-slate-500">
              AI-powered assessment
            </p>
          </div>

        </div>


        {/* Status */}

        <div className="flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5">

          <span className="h-2 w-2 rounded-full bg-emerald-500" />

          <Activity
            size={14}
            className="text-emerald-700"
          />

          <span className="text-xs font-medium text-emerald-800">
            Model Online
          </span>

        </div>

      </div>
    </header>
  );
}

export default Header;