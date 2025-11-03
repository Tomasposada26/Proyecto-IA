import React, { useState } from "react";
import axios from "axios";

const categorias = ["videojuegos", "peliculas", "libros", "musica"];


function Chat() {
  const [categoria, setCategoria] = useState("");
  const [gustos, setGustos] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [modo, setModo] = useState("gustos"); // gustos, top10, buscar
  const [mensajes, setMensajes] = useState([]);
  const [resultados, setResultados] = useState([]);

  const enviar = async () => {
    if (modo === "gustos") {
      setMensajes([...mensajes, { autor: "usuario", texto: `Me gustan: ${gustos}` }]);
      const res = await axios.post("http://localhost:8000/recomendar", {
        categoria,
        gustos: gustos.split(",").map(g => g.trim())
      });
      setResultados(res.data.recomendaciones);
      setMensajes([...mensajes, { autor: "usuario", texto: `Me gustan: ${gustos}` }, { autor: "nea", texto: "Aquí tienes tus recomendaciones:" }]);
    } else if (modo === "top10") {
      setMensajes([...mensajes, { autor: "usuario", texto: `Muéstrame el top 10 de ${categoria}` }]);
      const res = await axios.get(`http://localhost:8000/top10/${categoria}`);
      setResultados(res.data.top10);
      setMensajes([...mensajes, { autor: "usuario", texto: `Muéstrame el top 10 de ${categoria}` }, { autor: "nea", texto: "Top 10 de la categoría:" }]);
    } else if (modo === "buscar") {
      setMensajes([...mensajes, { autor: "usuario", texto: `Busco: ${busqueda}` }]);
      const res = await axios.post("http://localhost:8000/buscar", {
        categoria,
        query: busqueda
      });
      setResultados(res.data.resultados);
      setMensajes([...mensajes, { autor: "usuario", texto: `Busco: ${busqueda}` }, { autor: "nea", texto: "Resultados de la búsqueda:" }]);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", fontFamily: "sans-serif" }}>
      <h2>NEA - Network Entertainment Administer</h2>
      <div>
        <label>Categoría: </label>
        <select value={categoria} onChange={e => setCategoria(e.target.value)}>
          <option value="">Selecciona</option>
          {categorias.map(cat => <option key={cat} value={cat}>{cat}</option>)}
        </select>
      </div>
      <div style={{ margin: "10px 0" }}>
        <label>Modo: </label>
        <select value={modo} onChange={e => setModo(e.target.value)}>
          <option value="gustos">Por gustos</option>
          <option value="top10">Top 10</option>
          <option value="buscar">Búsqueda detallada</option>
        </select>
      </div>
      {modo === "gustos" && (
        <div>
          <label>Gustos (separados por coma): </label>
          <input value={gustos} onChange={e => setGustos(e.target.value)} />
          <button onClick={enviar} disabled={!categoria || !gustos}>Enviar</button>
        </div>
      )}
      {modo === "buscar" && (
        <div>
          <label>Búsqueda (título, autor, etc): </label>
          <input value={busqueda} onChange={e => setBusqueda(e.target.value)} />
          <button onClick={enviar} disabled={!categoria || !busqueda}>Buscar</button>
        </div>
      )}
      {modo === "top10" && (
        <div>
          <button onClick={enviar} disabled={!categoria}>Ver Top 10</button>
        </div>
      )}
      <div style={{ marginTop: 20, background: "#f4f4f4", padding: 10, borderRadius: 8 }}>
        {mensajes.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.autor === "usuario" ? "right" : "left" }}>
            <b>{msg.autor === "usuario" ? "Tú" : "NEA"}:</b> {msg.texto}
          </div>
        ))}
        {resultados.length > 0 && (
          <div style={{ marginTop: 10 }}>
            <b>Resultados:</b>
            <ul>
              {resultados.map((rec, i) => (
                <li key={i} style={{ marginBottom: 8 }}>
                  <a href={rec.link} target="_blank" rel="noopener noreferrer"><b>{rec.nombre}</b></a>
                  {rec.autor && <span> | <b>Autor:</b> {rec.autor}</span>}
                  {rec.director && <span> | <b>Director:</b> {rec.director}</span>}
                  {rec.artista && <span> | <b>Artista:</b> {rec.artista}</span>}
                  {rec.plataforma && <span> | <b>Plataforma:</b> {rec.plataforma}</span>}
                  {rec.calificacion && <span> | <b>Calificación:</b> {rec.calificacion}</span>}
                  {rec.reseña && <div><b>Reseña:</b> {rec.reseña}</div>}
                  {rec.sinopsis && <div><b>Sinopsis:</b> {rec.sinopsis}</div>}
                  {rec.tags && <div><b>Tags:</b> {rec.tags.join(", ")}</div>}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;
