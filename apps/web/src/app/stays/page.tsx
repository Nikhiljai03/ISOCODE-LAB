"use client";
import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, Users, Wifi, Coffee } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { api } from "@/lib/api";

const imagery: Record<string, string> = {
  ESTATE_ROOM: "photo-1600607687939-ce8a6c25118c",
  COFFEE_VILLA: "photo-1600566753086-00f18fb6b3ea",
};
const fallback = [{ id: "demo-room", code: "ESTATE_ROOM", name: "Estate Room", physical_inventory_count: 64 }, { id: "demo-villa", code: "COFFEE_VILLA", name: "Coffee Villa", physical_inventory_count: 12 }];

type Category = { id:string; code:string; name:string; physical_inventory_count:number };
export default function StaysPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [error, setError] = useState("");
  useEffect(() => { api<Category[]>("/api/v1/accommodations").then(setCategories).catch((e:Error) => setError(e.message)); }, []);
  const stays = categories.length ? categories : fallback;
  const [filter, setFilter] = useState<"all" | "villa">("all");
  const visibleStays = filter === "villa" ? stays.filter(stay => /villa/i.test(`${stay.code} ${stay.name}`)) : stays;
  return <main className="min-h-screen bg-[#f5f2ea] pb-24"><div className="relative h-[360px] bg-[#172b23] text-white"><Image src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1800&q=85" alt="Coffee estate" fill priority className="object-cover opacity-55"/><div className="absolute inset-0 bg-black/20"/><SiteHeader dark/><div className="absolute bottom-12 left-5 md:left-16"><p className="text-[10px] font-bold uppercase tracking-[.3em] text-white/70">The estate collection</p><h1 className="font-display mt-3 text-6xl md:text-8xl">Stay awhile.</h1></div></div>
    <div className="mx-auto max-w-[1400px] px-5 pt-10 md:px-10 lg:px-16"><div className="mb-10 flex flex-wrap items-center justify-between gap-4 border-b border-[#172b23]/15 pb-5"><p className="text-xs text-[#5b625b]">{error ? "Live catalogue unavailable — displaying presentation categories." : "Rooms and villas configured in the live reservation system."}</p><div className="flex gap-2"><button onClick={() => setFilter("all")} aria-pressed={filter === "all"} className={`border px-4 py-2 text-[10px] font-bold uppercase tracking-[.15em] ${filter === "all" ? "border-[#172b23] bg-[#172b23] text-white" : "border-[#172b23]/20"}`}>All stays</button><button onClick={() => setFilter("villa")} aria-pressed={filter === "villa"} className={`border px-4 py-2 text-[10px] font-bold uppercase tracking-[.15em] ${filter === "villa" ? "border-[#172b23] bg-[#172b23] text-white" : "border-transparent"}`}>Villa</button></div></div>
      {error && <p role="alert" className="mb-6 border-l-2 border-[#a87950] bg-[#e6ddcc]/60 px-4 py-3 text-sm">{error}</p>}
      <div className="grid gap-12 lg:grid-cols-2">{visibleStays.map((stay, index) => <article key={stay.id} className="group"><Link href={`/stays/${stay.id === "demo-room" ? "estate-room" : stay.id === "demo-villa" ? "coffee-villa" : stay.id}`}><div className="relative aspect-[4/3] overflow-hidden"><Image src={`https://images.unsplash.com/${imagery[stay.code] ?? "photo-1600566753086-00f18fb6b3ea"}?auto=format&fit=crop&w=1400&q=85`} alt={`${stay.name} at ARANYA`} fill sizes="50vw" className="object-cover saturate-[.82] transition-transform duration-[1200ms] ease-out group-hover:scale-[1.045] group-hover:saturate-100"/><span className="absolute right-5 top-5 bg-[#f5f2ea] px-4 py-2 text-[10px] font-bold uppercase tracking-[.14em] text-[#172b23]">{index === 0 ? "Garden outlook" : "Private terrace"}</span></div></Link><div className="flex items-start justify-between gap-6 border-b border-[#172b23]/15 py-7"><div><p className="text-[10px] font-bold uppercase tracking-[.18em] text-[#a87950]">{index === 0 ? "Estate collection" : "Villa collection"}</p><Link href={`/stays/${stay.id === "demo-room" ? "estate-room" : stay.id === "demo-villa" ? "coffee-villa" : stay.id}`}><h2 className="font-display mt-2 text-4xl text-[#172b23]">{stay.name}</h2></Link><div className="mt-4 flex gap-5 text-xs text-[#666c66]"><span className="flex items-center gap-1.5"><Users size={15}/> {index === 0 ? "2" : "4"} guests</span><span className="flex items-center gap-1.5"><Wifi size={15}/> Wi-Fi</span><span className="flex items-center gap-1.5"><Coffee size={15}/> Estate coffee</span></div></div><Link href={`/book?stay=${stay.id}`} className="mt-2 flex items-center gap-2 border-b border-[#172b23] pb-2 text-[10px] font-bold uppercase tracking-[.15em] text-[#172b23]">Reserve <ArrowRight size={15}/></Link></div></article>)}</div>
    </div>
  </main>;
}
