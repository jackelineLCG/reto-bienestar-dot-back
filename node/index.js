const axios = require('axios');

const usuario = {
  edad: 18,
  sexo: 'masculino'
};

const productos = [
  {
    id: 1,
    descripcion: 'zumba nivel principiante'
  },
  {
    id: 2,
    descripcion: 'Ruta: Positive food'
  }
];

async function obtenerDescripcionesAtractivas(productos, usuario) {
  try {
    for (let producto of productos) {
      const descripcionAtractiva = await generarDescripcionAI21(producto.descripcion, usuario);
      producto.descripcionAtractiva = descripcionAtractiva;
    }
    return productos;
  } catch (error) {
    console.error('Error al obtener descripciones atractivas:', error);
    throw error;
  }
}

async function generarDescripcionAI21(descripcionProducto, usuario) {
  try {
    const apiKey = 'YOUR_API_KEY';
    const url = 'https://api.ai21.com/studio/v1/j2-ultra/complete';

    const params = {
      prompt: `Genera una descripción atractiva para un producto. Descripción del producto: ${descripcionProducto}. Edad del usuario: ${usuario.edad}. Sexo del usuario: ${usuario.sexo}.`,
      numResults: 1,
      maxTokens: 60,
      temperature: 0.7,
      topP: 0.9
    };

    const response = await axios.post(url, params, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });

    const descripcionAtractiva = response.data.completions[0].data.text.trim();
    return descripcionAtractiva;
  } catch (error) {
    console.error('Error al generar descripción atractiva:', error);
    throw error;
  }
}

obtenerDescripcionesAtractivas(productos, usuario)
  .then(productosConDescripciones => {
    console.log('Productos con descripciones atractivas:');
    console.log(productosConDescripciones);
  })
  .catch(error => {
    console.error('Error en la ejecución:', error);
  });
