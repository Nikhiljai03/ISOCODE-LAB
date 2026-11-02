"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { CalendarDays, Users } from "lucide-react";

export function AvailabilityBar() {
  const router = useRouter();
  const [arrival, setArrival] = useState("");
  const [departure, setDeparture] = useState("");
  const submit = () => router.push(`/stays${arrival && departure ? `?arrival=${arrival}&departure=${departure}` : ""}`);
  return (
    <div className="mx-auto grid max-w-5xl grid-cols-1 divide-y divide-[#172B23]/10 bg-[#f5f2ea] text-[#172B23] shadow-[0_22px_60px_rgba(0,0,0,.18)] md:grid-cols-[1fr_1fr_.7fr_auto] md:divide-x md:divide-y-0">
      <label className="flex items-center gap-3 px-5 py-3"><CalendarDays size={19}/><span className="w-full"><small className="block text-[9px] font-bold uppercase tracking-[.16em]">Arrival</small><input aria-label="Arrival date" type="date" value={arrival} onChange={e=>setArrival(e.target.value)} className="w-full bg-transparent font-display text-lg outline-none"/></span></label>
      <label className="flex items-center gap-3 px-5 py-3"><CalendarDays size={19}/><span className="w-full"><small className="block text-[9px] font-bold uppercase tracking-[.16em]">Departure</small><input aria-label="Departure date" type="date" min={arrival} value={departure} onChange={e=>setDeparture(e.target.value)} className="w-full bg-transparent font-display text-lg outline-none"/></span></label>
      <label className="flex items-center gap-3 px-5 py-4"><Users size={19}/><span><small className="block text-[9px] font-bold uppercase tracking-[.16em]">Guests</small><span className="font-display text-xl">2 guests</span></span></label>
      <button onClick={submit} className="flex min-h-16 items-center justify-center bg-[#172B23] px-8 text-[11px] font-bold uppercase tracking-[.17em] text-white transition-colors hover:bg-[#243B30]">Check availability</button>
    </div>
  );
}
