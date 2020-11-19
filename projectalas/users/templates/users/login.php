{% extends "users/base2.php" %}
{% load crispy_forms_tags %}
{% block content %}
<br>
<br>
<br>

<br>

<br>
<br>

    <div class="sufee-login d-flex align-content-center flex-wrap">
        <div class="container">
            <div class="login-content">
                <!-- <div class="login-logo">
                    <a href="index.html">
                        <img class="align-content" src="images/logo.png" alt="">
                    </a>
                </div> -->
                <div class="login-form">

                    <form method="POST" id="loginForm">
                          {% csrf_token %}
                            <fieldset class="form-group">
                                    {{ form|crispy }}
                            </fieldset>
                            <div class="text-center">
                              <button class="btn btn-success loginbtn">Masuk Akun</button>
                          </div>
                          <div class="register-link m-t-15 text-center">
                              <p>Tidak memiliki akun ? <a href="{% url 'register' %}"> Daftar</a></p>
                          </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

{% endblock %}
