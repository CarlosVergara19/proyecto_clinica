-- ============================================================
-- Esquema de la base de datos
-- ============================================================
-- Ejecutar en Supabase -> SQL Editor antes que cualquier otro script.
--
-- Diseño: la aplicación corre del lado del servidor (Streamlit), así que
-- accede con una clave secreta que omite RLS. Las tablas quedan con RLS
-- activo y sin políticas, de modo que las claves publicables no pueden
-- leer ni escribir nada.
-- ============================================================


-- ── Equipos ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.equipos (
    id               TEXT PRIMARY KEY,          -- formato CRSJ001, CRSJ002...
    ubicacion        TEXT,
    unidad_funcional TEXT,
    usuario_cargo    TEXT,
    procesador       TEXT,
    espacio          TEXT,
    memoria_ram      TEXT,
    monitor          TEXT,
    nombre_equipo    TEXT,
    estado           TEXT,                      -- ACTIVO | MANTENIMIENTO | BAJA
    anydesk          TEXT,
    observacion      TEXT
);


-- ── Historial de mantenimientos e incidencias ────────────────
CREATE TABLE IF NOT EXISTS public.historial (
    id_registro BIGSERIAL PRIMARY KEY,
    id_equipo   TEXT REFERENCES public.equipos (id) ON DELETE CASCADE,
    fecha       DATE NOT NULL,
    tipo        TEXT,
    descripcion TEXT,
    tecnico     TEXT
);

CREATE INDEX IF NOT EXISTS idx_historial_equipo ON public.historial (id_equipo);
CREATE INDEX IF NOT EXISTS idx_historial_fecha  ON public.historial (fecha DESC);


-- ── Seguridad ────────────────────────────────────────────────
-- Sin políticas asociadas, RLS bloquea todo acceso que no venga de la
-- clave secreta del servidor.
ALTER TABLE public.equipos   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.historial ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.equipos   FORCE ROW LEVEL SECURITY;
ALTER TABLE public.historial FORCE ROW LEVEL SECURITY;


-- ── Comprobación ─────────────────────────────────────────────
-- rowsecurity debe ser true y politicas debe ser 0.
SELECT tablename, rowsecurity FROM pg_tables
WHERE schemaname = 'public' AND tablename IN ('equipos', 'historial');

SELECT COUNT(*) AS politicas FROM pg_policies WHERE schemaname = 'public';
