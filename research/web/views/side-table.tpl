% if not row:
  No data
% else:
  <table class="table table-striped table-hover">
    <thead>
      <tr>
        <th>Field</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
%   for key in row.keys():
      <tr>
        <td>{{key}}</td>
%     if key == 'symbol':
        <td><a href="/stock/{{row[key]}}" target="_blank">{{row[key]}}</a></td>
%     elif key == 'url':
        <td><a href="{{row[key]}}" target="_blank">website</a></td>
%     elif key == 'yahoo_url':
        <td><a href="{{row[key]}}" target="_blank">yahoo</a></td>
%     else:
        <td>{{row[key]}}</td>
%     end
      </tr>
%   end
    </tbodY>
  </table>
% end
