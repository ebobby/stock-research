% rebase('layout.tpl', title='Stock Analysis')

% if len(rows) == 0:
  No data
% else:
  <table class="table table-striped table-hover table-scroll">
    <thead>
      <tr>
         <th>#</th>
%   for col in list(rows[0].keys()):
         <th style="min-width: 120px">{{' '.join(w.capitalize() for w in col.split('_'))}}</th>
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
%       elif key in ['return_on_investment','rate_of_return', 'cagr', 'return_on_retained_earnings', 'earnings_growth']:
          <td>{{f"{round(float(row[key]) * 100.0, 2)}%"}}</td>
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
