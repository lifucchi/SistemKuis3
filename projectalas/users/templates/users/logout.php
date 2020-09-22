{% extends "users/base2.php" %}
{% load crispy_forms_tags %}
      {% block content %}
	<div class="error-pagewrap">
		<div class="error-page-int">
			<div class="text-center m-b-md custom-login">
				<h3>TOLONG MASUK AKUN TERLEBIH DAHULU</h3>
				<!-- <p>This is the best app ever!</p> -->
			</div>
			<div class="content-error">
				<div class="hpanel">
              <div class="panel-body">
                <h2>Anda sudah keluar</h2>
                  <br>
                  <div class="border-top pt-3">
                  <small class="text-muted">Masuk ?
                        <a class="btn btn-default " href="{% url 'login' %}">Masuk Akun</a>
                </small>
              </div>
              
              </div>
          </div>
			</div>
			<div class="text-center login-footer">
        <div class="border-top pt-3">
        <!-- <small class="text-muted">Belum memiliki akun? -->
              <p>Belum memiliki akun? <a href="{% url 'register' %}">Daftar</a></p>
        <!-- </small> -->
      </div>


				<p>Copyright © 2018. All rights reserved. Template by <a href="https://colorlib.com/wp/templates/">Colorlib</a></p>
			</div>
		</div>
    </div>

      {% endblock %}
