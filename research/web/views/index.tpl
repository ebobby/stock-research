% rebase('layout.tpl', title='Analysis')

% if len(rows) == 0:
  No data
% else:
  <table class="table table-striped table-hover table-scroll">
    <thead>
      <tr>
         <th>#</th>
%   for col in list(rows[0].keys()):
         <th>{{col}}</th>
%   end
      </tr>
    </thead>
    <tbody>
%   for i, row in enumerate(rows):
      <tr>
        <td>{{i+1}}</td>
%     for key in row.keys():
%       if key == 'symbol':
          <td><a href="/stock/{{row[key]}}" target="_blank">{{row[key]}}</a></td>
%       elif key == 'url':
          <td><a href="{{row[key]}}" target="_blank">website</a></td>
%       elif key == 'yahoo_url':
          <td><a href="{{row[key]}}" target="_blank">yahoo</a></td>
%       else:
         <td title="{{key}} for {{row[0]}}">{{row[key]}}</td>
%       end
%     end
      </tr>
%   end
    </tbodY>
  </table>
% end
