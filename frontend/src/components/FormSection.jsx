function FormSection({
    icon: Icon,
    title,
    description,
    children,
  }) {
    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
  
        {/* Section header */}
  
        <div className="mb-6 flex items-start gap-3">
  
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-800">
            <Icon size={20} />
          </div>
  
          <div>
            <h2 className="text-lg font-semibold tracking-tight text-slate-900">
              {title}
            </h2>
  
            <p className="mt-1 text-sm text-slate-500">
              {description}
            </p>
          </div>
  
        </div>
  
  
        {/* Fields */}
  
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          {children}
        </div>
  
      </section>
    );
  }
  
  export default FormSection;