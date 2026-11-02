import Link from "next/link";

export function SiteHeader({ dark = false }: { dark?: boolean }) {
  const text = dark ? "text-white" : "text-[#172B23]";
  return (
    <header className={`absolute inset-x-0 top-0 z-30 flex items-center justify-between px-5 py-5 md:px-10 lg:px-16 ${text}`}>
      <Link href="/" className="font-display text-[28px] tracking-[.24em]">ARANYA</Link>
      <nav className="hidden items-center gap-8 text-[11px] font-semibold uppercase tracking-[.18em] md:flex">
        <Link href="/stays" className="transition-opacity hover:opacity-70">Stay</Link>
        <Link href="/#experience" className="transition-opacity hover:opacity-70">Experience</Link>
        <Link href="/#gather" className="transition-opacity hover:opacity-70">Gather</Link>
        <Link href="/staff" className="transition-opacity hover:opacity-70">Reservations</Link>
      </nav>
      <Link href="/stays" className="border-b border-current pb-1 text-[11px] font-bold uppercase tracking-[.16em]">Reserve</Link>
    </header>
  );
}
