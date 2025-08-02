-- TICKETS DE ATENCIÓN
CREATE TABLE tickets_atencion (
    TicketID UUID PRIMARY KEY,
    FechaHora TIMESTAMP NOT NULL,
    ClienteID UUID NOT NULL,
    Canal VARCHAR(50),
    SucursalID VARCHAR(20),
    AsesorID UUID,
    TipoConsulta VARCHAR(50),
    Subtipo VARCHAR(50),
    Estado VARCHAR(20),
    TiempoRespuesta INT,
    TiempoResolucion INT,
    SatisfaccionCliente INT,
    Comentario TEXT,
    Etiquetas TEXT[],
    Adjunto TEXT
);

-- ENCUESTAS DE SATISFACCIÓN
CREATE TABLE encuestas_satisfaccion (
    EncuestaID UUID PRIMARY KEY,
    FechaEnvio DATE,
    FechaRespuesta DATE,
    ClienteID UUID NOT NULL,
    TicketID UUID,
    NPS INT,
    PuntuacionGeneral INT,
    FacilidadProceso INT,
    RapidezAtencion INT,
    AmabilidadAsesor INT,
    ResolucionProblema INT,
    ComentarioLibre TEXT,
    CanalEncuesta VARCHAR(20),
    EmojiSentimiento VARCHAR(10)
);

-- RESEÑAS ONLINE
CREATE TABLE reseñas_online (
    ReseñaID UUID PRIMARY KEY,
    Plataforma VARCHAR(50),
    FechaPublicacion DATE,
    ClienteID UUID,
    NombreUsuario VARCHAR(100),
    SucursalID VARCHAR(20),
    Puntaje INT,
    Comentario TEXT,
    Likes INT,
    RespuestasBanco TEXT,
    PalabrasClave TEXT[],
    Idioma VARCHAR(10),
    Origen TEXT
);

-- LLAMADAS CALL CENTER
CREATE TABLE llamadas_callcenter (
    LlamadaID UUID PRIMARY KEY,
    FechaHoraInicio TIMESTAMP,
    FechaHoraFin TIMESTAMP,
    ClienteID UUID,
    AsesorID UUID,
    DuracionSegundos INT,
    Motivo VARCHAR(100),
    Resumen TEXT,
    Transcripcion TEXT,
    Sentimiento VARCHAR(10),
    PalabrasClave TEXT[],
    AudioURL TEXT
);

-- LIBRO DE RECLAMACIONES
CREATE TABLE libro_reclamaciones (
    ReclamoID UUID PRIMARY KEY,
    Fecha DATE,
    ClienteID UUID,
    TipoDocumento VARCHAR(20),
    Canal VARCHAR(20),
    Motivo VARCHAR(100),
    Descripcion TEXT,
    Estado VARCHAR(20),
    FechaRespuesta DATE,
    Resolucion TEXT,
    TiempoResolucionDias INT,
    Responsable VARCHAR(50)
);

-- WHATSAPP CORPORATIVO
CREATE TABLE whatsapp_corporativo (
    MsgID UUID PRIMARY KEY,
    FechaHora TIMESTAMP,
    ClienteID UUID,
    AsesorID UUID,
    Direccion VARCHAR(20),
    Canal VARCHAR(50),
    TipoMensaje VARCHAR(20),
    Contenido TEXT,
    URLArchivo TEXT,
    DuracionSegundos INT,
    EstadoMensaje VARCHAR(20),
    Sentimiento VARCHAR(10),
    PalabrasClave TEXT[]
);
