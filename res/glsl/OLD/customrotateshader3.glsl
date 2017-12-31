
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

/*custom attributes*/
/*
attribute float x_trans;
attribute float y_trans;
attribute float x_shear;
*/

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

void main (void) {
  
  frag_color = color * vec4(1.0, 1., 1.0, opacity);
  tex_coord0 = uvs;

  /*Custom sprite rotation in radians*/
  int reverse_x = 0;
  int reverse_y = 0;
  
  float a_sin = sin(rot);
  float a_cos = cos(rot);
  mat4 rot_mat = mat4(a_cos, -a_sin, 0.0, 0.0,
		      a_sin, a_cos, 0.0, 0.0,
		      0.0, 0.0, 1.0, 0.0,
		      0.0, 0.0, 0.0, 1.0 );

  float x_trans = 1.0;
  float y_trans = 1.0;
  float x_shear = 0.0;
  float y_shear = 0.0;
  mat4 trans_mat = mat4(y_trans, x_shear,  0.0,  center.x,
			y_shear, x_trans,  0.0,  center.y,
			0.0,     0.0,      1.0,  0.0,
			0.0,     0.0,      0.0,  1.0);
  
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
  float rboost = 0.2;
  float gboost = 0.0;
  float bboost = 0.2;
  int has_white_edge = 0;
  
  if (pixel_color[0] > 0.025 || pixel_color[1] > 0.025 || pixel_color[2] > 0.025){
    pixel_color[0] = mod(pixel_color[0]+rboost,1.0);
    pixel_color[1] = mod(pixel_color[1]+gboost,1.0);
    pixel_color[2] = mod(pixel_color[2]+bboost,1.0);
  }

  /*white edge effect for damage animation*/
  if (has_white_edge == 1){
    if (pixel_color[0] < 0.01 || pixel_color[1] < 0.01 || pixel_color[2] < 0.01){
      pixel_color[0] = 1.0;
      pixel_color[1] = 1.0;
      pixel_color[2] = 1.0;
    }
  }
  gl_FragColor =vec4(pixel_color[0], pixel_color[1], pixel_color[2], pixel_color[3]);
    
  
}
