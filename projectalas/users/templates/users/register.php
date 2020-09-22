
{% extends "users/base2.php" %}
{% load crispy_forms_tags %}
      {% block content %}

	<div class="error-pagewrap">
		<div class="error-page-int">
			<div class="text-center custom-login">
				<h3>Pendaftaran</h3>
			</div>
			<div class="content-error">
				<div class="hpanel">
                    <div class="panel-body">
                        <form method="post" action="#" id="loginForm">
                          {% csrf_token %}
                            <div class="row">
                                <fieldset class="form-group col-lg-12">

                                    {{ form|crispy }}
                                </fieldset>

                            </div>
                            <div class="text-center">
                                <button class="btn btn-success loginbtn">Daftar</button>
                            </div>
                        </form>
                        <br>
                        <!-- <div class="border-top pt-3"> -->
                            <!-- <small class="text-muted">Sudah memiliki akun? -->
                              <!-- <a class="ml-2" href"{% url 'login' %}">Sign In</a> -->
                              <!-- <a class="btn btn-default btn-block" href="{% url 'login' %}">Masuk Akun</a> -->
                            <!-- </small> -->
                      <!-- </div> -->

                    </div>
                </div>
			</div>
			<div class="text-center login-footer">
        <div class="border-top pt-3">
        <!-- <small class="text-muted">Belum memiliki akun? -->
              <p>Sudah memiliki akun? <a href="{% url 'login' %}">Masuk Akun</a></p>
        <!-- </small> -->
      </div>
    </br>
				<p>Copyright © 2018. All rights reserved. Template by <a href="https://colorlib.com/wp/templates/">Colorlib</a></p>
			</div>
		</div>
    </div>

  {% endblock %}
