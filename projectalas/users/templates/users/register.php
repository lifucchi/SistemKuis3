{% extends "users/base2.php" %}
{% load crispy_forms_tags %}
{% block content %}

    <div class="sufee-login d-flex align-content-center flex-wrap">
        <div class="container">
            <div class="login-content">
                <div class="login-logo">
                    <a href="index.html">
                        <img class="align-content" src="images/logo.png" alt="">
                    </a>
                </div>
                <div class="login-form">
                    <form method="post" action="#" id="loginForm">
                    {% csrf_token %}
                      <div class="row">
                          <fieldset class="form-group col-lg-12">

                              {{ form|crispy }}
                          </fieldset>

                      </div>

                      <button type="submit" class="btn btn-primary btn-flat m-b-30 m-t-30">Register</button>

                      <div class="register-link m-t-15 text-center">
                          <p>Sudah memiliki akun? <a href="{% url 'login' %}"> Masuk</a></p>
                      </div>

                  </form>
                </div>
            </div>
        </div>
    </div>

    {% endblock %}
