<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>List file Excel</title>
  <!-- Import Bootstrap CSS t? CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container my-4">
    <h1 class="mb-4 text-center">List file Excel</h1>
    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            File count objects
          </div>
          <ul class="list-group list-group-flush">
            {% for file in excel_files %}
            <li class="list-group-item">
              <a href="{{ url_for('download', folder='excel', filename=file) }}" class="text-decoration-none">
                {{ file }}
              </a>
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card shadow">
          <div class="card-header bg-success text-white">
            File Detection Log
          </div>
          <ul class="list-group list-group-flush">
            {% for file in detection_files %}
            <li class="list-group-item">
              <a href="{{ url_for('download', folder='detection', filename=file) }}" class="text-decoration-none">
                {{ file }}
              </a>
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
  </div>
  <!-- Import Bootstrap JS Bundle t? CDN -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
