function InputField({
    label,
    name,
    value,
    onChange,
    type = "number",
    placeholder,
    min,
    max,
    step,
    options,
    help,
    required = false,
  }) {
    return (
      <div className="flex flex-col gap-2">
  
        <label
          htmlFor={name}
          className="text-sm font-medium text-slate-700"
        >
          {label}
        </label>
  
  
        {options ? (
  
          <select
            id={name}
            name={name}
            value={value}
            onChange={onChange}
            required={required}
            className="h-11 rounded-xl border border-slate-200 bg-slate-50 px-3 text-sm text-slate-900 outline-none transition focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-600/10"
          >
  
            {options.map((option) => (
              <option
                key={option}
                value={option}
              >
                {option}
              </option>
            ))}
  
          </select>
  
        ) : (
  
          <input
            id={name}
            name={name}
            type={type}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            min={min}
            max={max}
            step={step}
            required={required}
            className="h-11 rounded-xl border border-slate-200 bg-slate-50 px-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-600/10"
          />
  
        )}
  
  
        {help && (
          <p className="text-xs text-slate-400">
            {help}
          </p>
        )}
  
      </div>
    );
  }
  
  export default InputField;