% rebase('layout.tpl', title=symbol)

<a href="/">back</a>
<p />
<div style="margin-bottom: 40px">
  <h4>Analysis</h4>
% include('table.tpl', rows=[buffettology])
</div>
<div style="margin-bottom: 40px">
  <h4>Averages</h4>
% include('table.tpl', rows=[averages])
</div>
<div style="margin-bottom: 40px">
  <h4>Stats</h4>
% include('table.tpl', rows=[stats])
</div>
<div style="margin-bottom: 40px">
  <h4>Annual performance</h4>
% include('table.tpl', rows=annual)
</div>
<div style="margin-bottom: 40px">
  <h4>Prices</h4>
% include('table.tpl', rows=prices)
</div>