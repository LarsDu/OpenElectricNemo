
---VERTEX SHADER---
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* vertex attributes */
attribute vec2     pos;
attribute vec2     uvs;
attribute float    rot;
attribute vec2     center;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

void main (void) {
  frag_color = color * vec4(1.0, 1., 1.0, opacity);
  tex_coord0 = uvs;
  float a_sin = sin(rot);
  float a_cos = cos(rot);
  mat4 rot_mat = mat4(a_cos, -a_sin, 0.0, 0.0,
		      a_sin, a_cos, 0.0, 0.0,
		      0.0, 0.0, 1.0, 0.0,
		      0.0, 0.0, 0.0, 1.0 );
  mat4 trans_mat = mat4(1.0, 0.0, 0.0, center.x,
			0.0, 1.0, 0.0, center.y,
			0.0, 0.0, 1.0, 0.0,
			0.0, 0.0, 0.0, 1.0);
  vec4 new_pos = vec4(pos.xy, 0.0, 1.0);
  vec4 trans_pos = new_pos * rot_mat * trans_mat;
  gl_Position = projection_mat * modelview_mat * trans_pos;

}


---FRAGMENT SHADER---
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

void main (void){
  /* Custom shader code here 
   *Test 1- Grayscale
   * vec4 pixel_color = frag_color*texture2D(texture0,tex_coord0);
   *float average = (pixel_color[0]+pixel_color[1]+pixel_color[2])/3.;
   *gl_FragColor = vec4(average,average,average,pixel_color[3]);
   *gl_FragColor = frag_color * texture2D(texture0, tex_coord0);*/

  /*Custom shader 2 - Neonify*/

  vec4 pixel_color = frag_color*texture2D(texture0,tex_coord0);
  float rboost = 0.0;
  float gboost = .00;
  float bboost = .50;
    
  float r_color = mod(pixel_color[0]+rboost,1.0);
  float g_color = mod(pixel_color[1]+gboost,1.0);
  float b_color = mod(pixel_color[2]+bboost,1.0);
  
  gl_FragColor =vec4(r_color, g_color, b_color, pixel_color[3]);
    
  
}

