% rebase('layout.tpl', title=symbol)

<div class="d-flex align-items-center">
  <div class="flex-shrink-0">
    <img class="rounded" src="{{profile['logo_url']}}" style="width: 100px"/>
  </div>
  <div class="flex-grow-1 ms-3">
    <h1>{{symbol}}</h1>
  </div>
</div>
<p />
<p />
<ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">Profile</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="analysis-tab" data-bs-toggle="tab" data-bs-target="#analysis" type="button" role="tab" aria-controls="analysis" aria-selected="true">Analysis</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="prices-tab" data-bs-toggle="tab" data-bs-target="#prices" type="button" role="tab" aria-controls="prices" aria-selected="true">Prices</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="annual-tab" data-bs-toggle="tab" data-bs-target="#annual" type="button" role="tab" aria-controls="annual" aria-selected="false">Annual Performance</button>
  </li>
</ul>
<div class="tab-content" id="myTabContent" style="padding-top: 20px;">
  <div class="tab-pane fade show active" id="profile" role="tabpanel" aria-labelledby="profile-tab">
    <div class="container">
      <div class="row">
        <div class="col-8">
          % include('side-table.tpl', row=profile)
        </div>
      </div>
    </div>
  </div>
  <div class="tab-pane fade" id="analysis" role="tabpanel" aria-labelledby="analysis-tab">
    <div class="container">
      <div class="row">
        <div class="col-4">
          <h5>Statistics</h5>
          % include('side-table.tpl', row=stats)
        </div>
        <div class="col-4">
          <h5>Buffettology</h5>
          % include('side-table.tpl', row=buffettology)
        </div>
        <div class="col-4">
          <h5>Averages</h5>
          % include('side-table.tpl', row=averages)
        </div>
      </div>
    </div>
  </div>
  <div class="tab-pane fade" id="prices" role="tabpanel" aria-labelledby="prices-tab">
    <div class="container">
      <div class="row">
        <div class="col-6">
          <h5>Prices</h5>
          % include('table.tpl', rows=prices, scroll=False)
        </div>
        <div class="col-6">
          <h5>Discounted Cash Flow</h5>
          % include('table.tpl', rows=[dcf], scroll=False)
        </div>
      </div>
    </div>
  </div>
  <div class="tab-pane fade" id="annual" role="tabpanel" aria-labelledby="annual-tab">
    % include('table.tpl', rows=annual)
  </div>
</div>
