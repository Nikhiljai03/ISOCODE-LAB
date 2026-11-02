"use client";
import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CalendarDays, Check, CreditCard, LoaderCircle } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { api } from "@/lib/api";

function BookingFlow() {
  const search = useSearchParams();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [arrival, setArrival] = useState("");
  const [departure, setDeparture] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [hold, setHold] = useState<{hold_id:string;booking_id:string;expires_at:string;total_amount:string}|null>(null);
  const [reference, setReference] = useState("");
  const category = search.get("stay") ?? "";

  async function createHold() {
    if (!arrival || !departure || !category || category.startsWith("demo-") || !email) { setError("Choose live stay dates and enter an email address. If backend accommodation data is unavailable, live inventory cannot be reserved."); return; }
    setLoading(true); setError("");
    try { setHold(await api(`/api/v1/holds?category_id=${category}&arrival=${arrival}&departure=${departure}&guest_email=${encodeURIComponent(email)}&guest_name=${encodeURIComponent(name)}`, {method:"POST",headers:{"Idempotency-Key":crypto.randomUUID()}})); setStep(2); }
    catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }
  async function confirmPayment() {
    if (!hold) return;
    setLoading(true); setError("");
    try { await api("/api/v1/payments/test/confirm", {method:"POST",body:JSON.stringify({booking_id:hold.booking_id,provider_payment_id:`TEST-${crypto.randomUUID()}`,provider_event_id:`EVT-${crypto.randomUUID()}`,amount:Number(hold.total_amount)})}); setReference(hold.booking_id); setStep(3); }
    catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  return <main className="min-h-screen bg-[#f5f2ea] pb-20"><SiteHeader /><div className="mx-auto max-w-6xl px-5 pt-28 md:px-10"><Link href="/stays" className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[.16em] text-[#172b23]"><ArrowLeft size={15}/> All stays</Link><div className="mt-10 grid gap-10 lg:grid-cols-[1fr_360px]">
    <section><div className="mb-10 flex gap-8 border-b border-[#172b23]/15">{["Your stay","Guest details","Payment"].map((label,i)=><button key={label} onClick={()=> i < step && setStep(i+1)} className={`pb-4 text-[10px] font-bold uppercase tracking-[.16em] ${step===i+1?"border-b-2 border-[#172b23] text-[#172b23]":"text-[#777d77]"}`}>0{i+1} {label}</button>)}</div>
      {step===1 && <div><p className="text-[10px] font-bold uppercase tracking-[.22em] text-[#a87950]">Reserve your stay</p><h1 className="font-display mt-3 text-5xl text-[#172b23] md:text-7xl">When shall we<br/>welcome you?</h1><div className="mt-10 grid gap-5 sm:grid-cols-2"><label className="text-[10px] font-bold uppercase tracking-[.15em]">Arrival<input type="date" value={arrival} onChange={e=>setArrival(e.target.value)} className="mt-3 w-full border border-[#172b23]/20 bg-white px-5 py-4 text-base font-normal normal-case"/></label><label className="text-[10px] font-bold uppercase tracking-[.15em]">Departure<input type="date" value={departure} min={arrival} onChange={e=>setDeparture(e.target.value)} className="mt-4 w-full border border-[#172b23]/20 bg-white px-5 py-4 text-base font-normal normal-case"/></label></div><button onClick={()=>{if(arrival&&departure)setStep(2)}} className="mt-8 bg-[#172b23] px-7 py-4 text-[10px] font-bold uppercase tracking-[.16em] text-white">Continue with stay details</button></div>}
      {step === 2 && (
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[.22em] text-[#a87950]">Guest details</p>
          <h1 className="font-display mt-3 text-5xl text-[#172b23]">Who is travelling?</h1>
          <div className="mt-8 grid gap-5 sm:grid-cols-2">
            <label className="text-xs font-semibold">Full name<input required value={name} onChange={e=>setName(e.target.value)} className="mt-2 w-full border border-[#172b23]/20 bg-white px-4 py-3"/></label>
            <label className="text-xs font-semibold">Email<input required type="email" value={email} onChange={e=>setEmail(e.target.value)} className="mt-2 w-full border border-[#172b23]/20 bg-white px-4 py-3"/></label>
          </div>
          <button disabled={loading} onClick={createHold} className="mt-8 flex items-center gap-2 bg-[#172b23] px-7 py-4 text-[10px] font-bold uppercase tracking-[.16em] text-white disabled:opacity-60">
            {loading && <LoaderCircle className="animate-spin" size={16}/>} 
            {loading ? "Creating hold" : "Reserve dates"}
          </button>
        </div>
      )}
      {step===3 && <div className="border border-[#172b23]/15 bg-white p-8"><div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#172b23] text-white"><Check/></div><p className="mt-7 text-[10px] font-bold uppercase tracking-[.22em] text-[#a87950]">Test payment accepted</p><h1 className="font-display mt-3 text-5xl text-[#172b23]">Your stay is confirmed.</h1><p className="mt-5 text-sm text-[#5b625b]">This confirmation was created by the backend payment lifecycle.</p><div className="mt-8 border-t border-[#172b23]/15 pt-5 text-sm">Reference <strong className="ml-3 font-mono">{reference}</strong></div></div>}
      {error&&<p role="alert" className="mt-6 border-l-2 border-red-700 bg-red-50 px-4 py-3 text-sm text-red-800">{error}</p>}
    </section>
    <aside className="h-fit border border-[#172b23]/15 bg-white p-6"><p className="text-[10px] font-bold uppercase tracking-[.18em] text-[#a87950]">Your reservation</p><h2 className="font-display mt-2 text-3xl text-[#172b23]">{category.startsWith("demo-")?"Select a live category":"ARANYA stay"}</h2><div className="mt-6 space-y-4 border-y border-[#172b23]/15 py-5 text-sm"><p className="flex items-center gap-3"><CalendarDays size={16}/> {arrival || "Arrival"} — {departure || "Departure"}</p><p>2 guests · 1 room</p></div><div className="py-5 text-xs text-[#5b625b]">Live room subtotal and GST are calculated by the backend after inventory is held. No rate is shown until confirmed by an API response.</div>{hold&&<button onClick={confirmPayment} disabled={loading} className="flex w-full items-center justify-center gap-2 bg-[#172b23] py-4 text-[10px] font-bold uppercase tracking-[.16em] text-white"><CreditCard size={16}/> Confirm test payment</button>}</aside>
  </div></div></main>;
}
export default function BookingPage(){return <Suspense><BookingFlow/></Suspense>}
