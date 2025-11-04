import React, { useState } from "react";
import axios from "axios";

// Available categories for recommendation
const categorias = ["videojuegos", "peliculas", "libros", "musica", "series"];
// Available recommendation methods
const metodos = [
  { value: "multimodal", label: "Multimodal" },
  { value: "cbf", label: "Basado en contenido" },
  { value: "cf", label: "Filtrado colaborativo" },
];

function Chat() {
  const [categoria, setCategoria] = useState("");
  const [gustos, setGustos] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [modo, setModo] = useState("gustos"); // 'gustos', 'top10', 'buscar'
  const [metodo, setMetodo] = useState("multimodal");
  const [mensajes, setMensajes] = useState([]);
  const [resultados, setResultados] = useState([]);
  // Filtros personalizados
  const [filtroAnio, setFiltroAnio] = useState("");
  const [filtroArtista, setFiltroArtista] = useState("");
  const [filtroPlataforma, setFiltroPlataforma] = useState("");
  const [filtroGenero, setFiltroGenero] = useState("");
  const [filtroAutor, setFiltroAutor] = useState("");

  const enviar = async () => {
    if (modo === "gustos") {
      setMensajes([
        ...mensajes,
        { autor: "usuario", texto: `Me gustan: ${gustos}` },
      ]);
      try {
        const res = await axios.post("http://localhost:8000/recomendar", {
          categoria,
          gustos: gustos.split(",").map((g) => g.trim()),
          metodo,
        });
        setResultados(res.data.recomendaciones);
        setMensajes([
          ...mensajes,
          { autor: "usuario", texto: `Me gustan: ${gustos}` },
          { autor: "nea", texto: "Aquí tienes tus recomendaciones:" },
        ]);
      } catch (err) {
        console.error(err);
      }
    } else if (modo === "top10") {
      setMensajes([
        ...mensajes,
        { autor: "usuario", texto: `Muéstrame el top 10 de ${categoria}` },
      ]);
      try {
        const res = await axios.get(
          `http://localhost:8000/top10/${categoria}`
        );
        setResultados(res.data.top10);
        setMensajes([
          ...mensajes,
          { autor: "usuario", texto: `Muéstrame el top 10 de ${categoria}` },
          { autor: "nea", texto: "Top 10 de la categoría:" },
        ]);
      } catch (err) {
        console.error(err);
      }
    } else if (modo === "buscar") {
      setMensajes([
        ...mensajes,
        { autor: "usuario", texto: `Busco: ${busqueda}` },
      ]);
      try {
        // Construir filtros según la categoría
        let filtros = {};
        if (categoria === "musica") {
          if (filtroAnio) filtros["año"] = filtroAnio;
          if (filtroArtista) filtros["artista"] = filtroArtista;
        } else if (categoria === "videojuegos") {
          if (filtroAnio) filtros["año"] = filtroAnio;
          if (filtroGenero) filtros["genero"] = filtroGenero;
          if (filtroPlataforma) filtros["plataforma"] = filtroPlataforma;
        } else if (categoria === "peliculas") {
          if (filtroAnio) filtros["año"] = filtroAnio;
          if (filtroGenero) filtros["genero"] = filtroGenero;
        } else if (categoria === "libros") {
          if (filtroAnio) filtros["año"] = filtroAnio;
          if (filtroGenero) filtros["genero"] = filtroGenero;
          if (filtroAutor) filtros["autor"] = filtroAutor;
        }
        const res = await axios.post("http://localhost:8000/buscar", {
          categoria,
          query: busqueda,
          filtros,
        });
  console.log('Resultados crudos backend:', res.data.resultados);
  setResultados(res.data.resultados);
        setMensajes([
          ...mensajes,
          { autor: "usuario", texto: `Busco: ${busqueda}` },
          { autor: "nea", texto: "Resultados de la búsqueda:" },
        ]);
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", fontFamily: "sans-serif" }}>
      <h2>NEA - Network Entertainment Administer</h2>
      {/* Category selection */}
      <div>
        <label>Categoría:&nbsp;</label>
        <select value={categoria} onChange={(e) => setCategoria(e.target.value)}>
          <option value="">Selecciona</option>
          {categorias.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>
      {/* Mode selection */}
      <div style={{ margin: "10px 0" }}>
        <label>Modo:&nbsp;</label>
        <select value={modo} onChange={(e) => setModo(e.target.value)}>
          <option value="gustos">Por gustos</option>
          <option value="top10">Top 10</option>
          <option value="buscar">Búsqueda detallada</option>
        </select>
      </div>
      {/* Method selection (only for gustos mode) */}
      {modo === "gustos" && (
        <div style={{ marginBottom: "10px" }}>
          <label>Método de recomendación:&nbsp;</label>
          <select value={metodo} onChange={(e) => setMetodo(e.target.value)}>
            {metodos.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label}
              </option>
            ))}
          </select>
        </div>
      )}
      {/* Input for gustos */}
      {modo === "gustos" && (
        <div>
          <label>Gustos (separados por coma):&nbsp;</label>
          <input value={gustos} onChange={(e) => setGustos(e.target.value)} />
          <button
            onClick={enviar}
            disabled={!categoria || gustos.trim() === ""}
            style={{ marginLeft: "8px" }}
          >
            Enviar
          </button>
        </div>
      )}
      {/* Input for search y filtros personalizados */}
      {modo === "buscar" && (
        <div>
          {/* Filtros para música */}
          {categoria === "musica" && (
            <div style={{ marginBottom: 8 }}>
              <label>Año:&nbsp;</label>
              <input
                placeholder="Ej: 2020"
                value={filtroAnio}
                onChange={(e) => setFiltroAnio(e.target.value)}
                style={{ width: 80, marginRight: 10 }}
              />
              <label>Artista:&nbsp;</label>
              <input
                placeholder="Ej: Shakira"
                value={filtroArtista}
                onChange={(e) => setFiltroArtista(e.target.value)}
                style={{ width: 120, marginRight: 10 }}
              />
            </div>
          )}
          {/* Filtros para videojuegos */}
          {categoria === "videojuegos" && (
            <div style={{ marginBottom: 8 }}>
              <label>Año:&nbsp;</label>
              <input
                placeholder="Ej: 2015"
                value={filtroAnio}
                onChange={(e) => setFiltroAnio(e.target.value)}
                style={{ width: 80, marginRight: 10 }}
              />
              <label>Género:&nbsp;</label>
              <input
                placeholder="Ej: deportes, acción, aventura"
                value={filtroGenero}
                onChange={(e) => setFiltroGenero(e.target.value)}
                style={{ width: 120, marginRight: 10 }}
              />
              <label>Plataforma:&nbsp;</label>
              <input
                placeholder="Ej: PS4, Xbox, PC"
                value={filtroPlataforma}
                onChange={(e) => setFiltroPlataforma(e.target.value)}
                style={{ width: 120, marginRight: 10 }}
              />
            </div>
          )}
          {/* Filtros para películas */}
          {categoria === "peliculas" && (
            <div style={{ marginBottom: 8 }}>
              <label>Año:&nbsp;</label>
              <input
                placeholder="Ej: 2010"
                value={filtroAnio}
                onChange={(e) => setFiltroAnio(e.target.value)}
                style={{ width: 80, marginRight: 10 }}
              />
              <label>Género:&nbsp;</label>
              <input
                placeholder="Ej: drama, comedia, terror"
                value={filtroGenero}
                onChange={(e) => setFiltroGenero(e.target.value)}
                style={{ width: 120, marginRight: 10 }}
              />
            </div>
          )}
          {/* Filtros para libros */}
          {categoria === "libros" && (
            <div style={{ marginBottom: 8 }}>
              <label>Año:&nbsp;</label>
              <input
                placeholder="Ej: 1999"
                value={filtroAnio}
                onChange={(e) => setFiltroAnio(e.target.value)}
                style={{ width: 80, marginRight: 10 }}
              />
              <label>Género:&nbsp;</label>
              <input
                placeholder="Ej: fantasía, novela, ciencia ficción"
                value={filtroGenero}
                onChange={(e) => setFiltroGenero(e.target.value)}
                style={{ width: 120, marginRight: 10 }}
              />
              <label>Autor:&nbsp;</label>
              <input
                placeholder="Ej: Gabriel García Márquez"
                value={filtroAutor}
                onChange={(e) => setFiltroAutor(e.target.value)}
                style={{ width: 160, marginRight: 10 }}
              />
            </div>
          )}
          <label>¿Qué quieres buscar? (puedes usar filtros)</label>
          <input
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            style={{ width: 300, marginRight: 10 }}
          />
          <button
            onClick={enviar}
            disabled={
              !categoria ||
              (busqueda.trim() === "" &&
                !filtroAnio &&
                !filtroArtista &&
                !filtroGenero &&
                !filtroPlataforma &&
                !filtroAutor)
            }
            style={{ marginLeft: "8px" }}
          >
            Enviar
          </button>
        </div>
      )}
      {/* Button for top10 */}
      {modo === "top10" && (
        <div>
          <button onClick={enviar} disabled={!categoria}>Ver Top 10</button>
        </div>
      )}
      {/* Display messages and results */}
      <div
        style={{ marginTop: 20, background: "#f4f4f4", padding: 10, borderRadius: 8 }}
      >
        {mensajes.map((msg, i) => (
          <div
            key={i}
            style={{ textAlign: msg.autor === "usuario" ? "right" : "left" }}
          >
            <b>{msg.autor === "usuario" ? "Tú" : "NEA"}:</b> {msg.texto}
          </div>
        ))}
        {resultados.length > 0 && (
          <div style={{ marginTop: 10 }}>
            <b>Resultados:</b>
            <ul>
              {resultados.map((rec, i) => {
                // Mostrar campos especiales para música
                if (categoria === "musica") {
                  return (
                    <li key={i} style={{ marginBottom: 8 }}>
                      <b>{rec["nombre"]}</b>
                      {rec["artista"] && (
                        <span>
                          &nbsp;|&nbsp;<b>Artista:</b> {rec["artista"]}
                        </span>
                      )}
                      {rec["año"] && (
                        <span>
                          &nbsp;|&nbsp;<b>Año:</b> {rec["año"]}
                        </span>
                      )}
                      {rec["streams"] && (
                        <span>
                          &nbsp;|&nbsp;<b>Streams:</b> {rec["streams"]}
                        </span>
                      )}
                      {rec["cover_url"] && rec["cover_url"] !== "Not Found" && (
                        <div>
                          <img src={rec["cover_url"]} alt="cover" style={{ width: 60, marginTop: 4 }} />
                        </div>
                      )}
                    </li>
                  );
                }
                // Otros casos (peliculas, libros, videojuegos)
                return (
                  <li key={i} style={{ marginBottom: 8 }}>
                    {/* Link to external page if available */}
                    {rec.link ? (
                      <a
                        href={rec.link}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <b>{rec.nombre}</b>
                      </a>
                    ) : (
                      <b>{rec.nombre}</b>
                    )}
                    {rec.autor && (
                      <span>
                        &nbsp;|&nbsp;<b>Autor:</b> {rec.autor}
                      </span>
                    )}
                    {rec.director && (
                      <span>
                        &nbsp;|&nbsp;<b>Director:</b> {rec.director}
                      </span>
                    )}
                    {rec.artista && (
                      <span>
                        &nbsp;|&nbsp;<b>Artista:</b> {rec.artista}
                      </span>
                    )}
                    {rec.plataforma && (
                      <span>
                        &nbsp;|&nbsp;<b>Plataforma:</b> {rec.plataforma}
                      </span>
                    )}
                    {rec.calificacion && (
                      <span>
                        &nbsp;|&nbsp;<b>Calificación:</b> {rec.calificacion}
                      </span>
                    )}
                    {rec.reseña && (
                      <div>
                        <b>Reseña:</b> {rec.reseña}
                      </div>
                    )}
                    {rec.sinopsis && (
                      <div>
                        <b>Sinopsis:</b> {rec.sinopsis}
                      </div>
                    )}
                    {rec.tags && rec.tags.length > 0 && (
                      <div>
                        <b>Tags:</b> {rec.tags.join(", ")}
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;