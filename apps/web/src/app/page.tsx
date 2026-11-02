import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { AvailabilityBar } from "@/components/availability-bar";

const image = (id: string) => `https://images.unsplash.com/${id}?auto=format&fit=crop&w=1800&q=85`;

export default function Home() {
  return (
    <main className="overflow-hidden bg-[#f5f2ea]">
      <section className="relative min-h-[760px] bg-[#172b23] text-white md:min-h-[820px]">
        <Image src={image("photo-1500530855697-b586d89ba3ee")} alt="Misty forest landscape" fill priority sizes="100vw" className="object-cover opacity-75" />
        <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(23,43,35,.42),rgba(23,43,35,.12)_45%,rgba(23,43,35,.72))]" />
        <SiteHeader dark />
        <div className="relative z-10 mx-auto flex min-h-[760px] max-w-[1400px] items-end px-5 pb-32 md:min-h-[820px] md:px-10 md:pb-36 lg:px-16">
          <div className="max-w-3xl reveal">
            <p className="mb-5 text-[10px] font-bold uppercase tracking-[.32em] text-white/80">Chikkamagaluru · Karnataka</p>
            <h1 className="font-display text-[58px] leading-[.84] sm:text-[76px] md:text-[104px]">Where the hills<br />slow time.</h1>
            <p className="mt-7 max-w-md text-sm leading-7 text-white/85">A private coffee-estate escape shaped by mist, old trees and unhurried days.</p>
            <Link href="/stays" className="mt-8 inline-flex items-center gap-4 border-b border-white pb-2 text-[11px] font-bold uppercase tracking-[.18em]">Reserve your stay <ArrowRight size={16}/></Link>
          </div>
        </div>
        <div className="absolute inset-x-0 bottom-[-46px] z-20 px-5"><AvailabilityBar /></div>
      </section>

      <section className="mx-auto grid max-w-[1400px] gap-12 px-5 pb-24 pt-32 md:grid-cols-[.85fr_1.15fr] md:px-10 md:pt-40 lg:px-16">
        <div className="relative aspect-[4/5] overflow-hidden md:mt-20 reveal"><Image src={image("photo-1441974231531-c6227db76b6e")} alt="Coffee estate beneath tall trees" fill sizes="45vw" className="object-cover" /></div>
        <div className="flex flex-col justify-center md:pl-16">
          <p className="text-[10px] font-bold uppercase tracking-[.28em] text-[#a87950]">Our estate</p>
          <h2 className="font-display mt-5 text-5xl leading-[.95] text-[#172b23] md:text-7xl">Rooted in nature,<br/><i>made for living.</i></h2>
          <p className="mt-8 max-w-lg text-sm leading-8 text-[#4f574f]">Set among layered coffee slopes, ARANYA brings together quiet architecture, estate-grown coffee and the particular calm of life at the edge of the Western Ghats.</p>
          <Link href="/stays" className="mt-8 inline-flex w-fit items-center gap-3 text-[11px] font-bold uppercase tracking-[.18em] text-[#172b23]">Discover the estate <ArrowRight size={16}/></Link>
        </div>
      </section>

      <section className="bg-[#172b23] px-5 py-24 text-white md:px-10 lg:px-16">
        <div className="mx-auto max-w-[1400px]">
          <div className="mb-12 flex items-end justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[.28em] text-[#d2b296]">A quieter kind of stay</p><h2 className="font-display mt-4 text-5xl md:text-7xl">Rooms & villas</h2></div><Link href="/stays" className="hidden border-b pb-2 text-[11px] font-bold uppercase tracking-[.16em] md:block">View all stays</Link></div>
          <div className="grid gap-5 md:grid-cols-[1.35fr_.65fr]">
            <Link href="/stays/estate-room" className="group relative min-h-[520px] overflow-hidden"><Image src={image("photo-1600607687939-ce8a6c25118c")} alt="Wooden estate villa interior" fill sizes="60vw" className="object-cover transition-transform duration-700 group-hover:scale-[1.02]"/><div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 p-7"><h3 className="font-display text-4xl">Estate Room</h3><p className="mt-2 text-xs uppercase tracking-[.16em] text-white/70">2 guests · Garden outlook</p></div></Link>
            <Link href="/stays/coffee-villa" className="group relative min-h-[520px] overflow-hidden"><Image src={image("photo-1600566753086-00f18fb6b3ea")} alt="Premium villa living room" fill sizes="40vw" className="object-cover transition-transform duration-700 group-hover:scale-[1.02]"/><div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 p-7"><h3 className="font-display text-4xl">Coffee Villa</h3><p className="mt-2 text-xs uppercase tracking-[.16em] text-white/70">4 guests · Private terrace</p></div></Link>
          </div>
        </div>
      </section>

      <section id="experience" className="mx-auto max-w-[1400px] px-5 py-24 md:px-10 lg:px-16">
        <div className="grid items-center gap-12 md:grid-cols-2"><div><p className="text-[10px] font-bold uppercase tracking-[.28em] text-[#a87950]">Estate rhythm</p><h2 className="font-display mt-5 text-5xl leading-[.95] text-[#172b23] md:text-7xl">Days shaped<br/>by the hills.</h2><p className="mt-7 max-w-md text-sm leading-8 text-[#4f574f]">Walk the plantation at first light, follow the aroma to a cup brewed moments away, or let an afternoon disappear beside the infinity pool.</p></div><div className="grid grid-cols-2 gap-4"><div className="relative col-span-2 aspect-[16/10] overflow-hidden"><Image src={image("photo-1507525428034-b723cf961d3e")} alt="Estate pool landscape" fill sizes="50vw" className="object-cover" /></div><div className="relative aspect-square"><Image src={image("photo-1445116572660-236099ec97a0")} alt="Coffee being prepared" fill sizes="25vw" className="object-cover" /></div><div className="flex items-center bg-[#e6ddcc] p-6"><p className="font-display text-3xl text-[#172b23]">Harvest, roast,<br/><i>pour, repeat.</i></p></div></div></div>
      </section>

      <section id="gather" className="relative min-h-[620px] text-white"><Image src={image("photo-1519167758481-83f550bb49b3")} alt="Gathering space at dusk" fill sizes="100vw" className="object-cover"/><div className="absolute inset-0 bg-[#172b23]/55"/><div className="relative mx-auto flex min-h-[620px] max-w-[1400px] items-center px-5 md:px-10 lg:px-16"><div className="max-w-xl"><p className="text-[10px] font-bold uppercase tracking-[.28em] text-[#d2b296]">Gather at ARANYA</p><h2 className="font-display mt-5 text-6xl leading-[.9] md:text-8xl">Meaningful<br/>moments, away.</h2><p className="mt-7 max-w-md text-sm leading-7 text-white/80">Restful weddings and focused retreats in the green quiet of the estate.</p><Link href="/enquiries" className="mt-8 inline-flex items-center gap-3 border-b pb-2 text-[11px] font-bold uppercase tracking-[.18em]">Plan your gathering <ArrowRight size={16}/></Link></div></div></section>

      <footer className="bg-[#243b30] px-5 py-16 text-white md:px-10 lg:px-16"><div className="mx-auto flex max-w-[1400px] flex-col gap-10 md:flex-row md:items-end md:justify-between"><div><div className="font-display text-4xl tracking-[.22em]">ARANYA</div><p className="mt-4 text-xs text-white/60">Coffee Hills · Chikkamagaluru · Karnataka</p></div><div className="flex gap-8 text-[11px] font-semibold uppercase tracking-[.15em]"><Link href="/stays">Stay</Link><Link href="/staff">Reservations</Link><Link href="/enquiries">Enquiries</Link></div></div></footer>
    </main>
  );
}
