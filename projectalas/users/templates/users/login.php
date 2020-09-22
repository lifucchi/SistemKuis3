{% extends "users/base2.php" %}
{% load crispy_forms_tags %}
      {% block content %}
	<div class="error-pagewrap">
		<div class="error-page-int">
			<div class="text-center m-b-md custom-login">
				<h3>TOLONG MASUK TERLEBIH DAHULU</h3>
				<!-- <p>This is the best app ever!</p> -->
			</div>
			<div class="content-error">
				<div class="hpanel">
                    <div class="panel-body">
                        <form method="POST" id="loginForm">
                          {% csrf_token %}
                            <fieldset class="form-group">
                                <!-- <label class="control-label" for="username">Username</label>
                                <input type="text" placeholder="example@gmail.com" title="Please enter you username" required="" value="" name="username" id="username" class="form-control">
                                <span class="help-block small">Your unique username to app</span> -->
                                    {{ form|crispy }}
                            </fieldset>
                            <!-- <div class="form-group">
                                <label class="control-label" for="password">Password</label>
                                <input type="password" title="Please enter your password" placeholder="******" required="" value="" name="password" id="password" class="form-control">
                                <span class="help-block small">Yur strong password</span>
                            </div> -->
                            <!-- <div class="checkbox login-checkbox">
                                <label>
										<input type="checkbox" class="i-checks"> Remember me </label>
                                <p class="help-block small">(if this is a private computer)</p>
                            </div> -->
                            <div class="text-center">
                              <button class="btn btn-success loginbtn">Masuk Akun</button>
                          </div>

                        </form>
                        <br>
                        <div class="border-top pt-3">
                        <!-- <small class="text-muted">Belum memiliki akun?
                              <p><a href="{% url 'register' %}">Daftar</a></p>
                        </small> -->
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
      <br>
				<p>Copyright © 2018. All rights reserved. Template by <a href="https://colorlib.com/wp/templates/">Colorlib</a></p>
			</div>
		</div>
    </div>

      {% endblock %}
